import { readFileSync } from 'node:fs'

const files = {
  lidar: 'awaken-a1-lidar-80m-10min.csv',
  scada: 'awaken-wt041-scada-1min.csv',
  paired: 'awaken-a1-wt041-2023-08-24.csv'
}

// The bundled teaching extracts use plain, unquoted fields.
function readRows(path) {
  const [header, ...lines] = readFileSync(path, 'utf8').trim().split(/\r?\n/)
  const fields = header.split(',')
  return lines.map(line => {
    const values = line.split(',')
    if (values.length !== fields.length || line.includes('"')) throw new Error('Unexpected teaching CSV format: ' + path)
    return Object.fromEntries(fields.map((field, i) => [field, values[i]]))
  })
}

function num(value) {
  if (!value?.trim() || !Number.isFinite(Number(value))) throw new Error('Invalid value in teaching case')
  return Number(value)
}

const mean = values => values.reduce((sum, value) => sum + value, 0) / values.length
const windowDate = '2023-08-24 '
const split = windowDate + '16:00'
const minutes = Array.from({ length: 10 }, (_, i) => '00:0' + i)

function powerCurve(rows, source) {
  const bins = new Map()
  for (const row of rows) {
    const bin = Math.floor(num(row[source]))
    if (!bins.has(bin)) bins.set(bin, [])
    bins.get(bin).push(row)
  }
  return new Map([...bins].filter(([, rows]) => rows.length >= 3).map(([bin, rows]) => [
    bin,
    { bin, count: rows.length, speed: mean(rows.map(r => num(r[source]))), power: mean(rows.map(r => num(r.power_kw))) }
  ]))
}

function estimate(curve, speed) {
  for (const [bin, left] of curve) {
    const right = curve.get(bin + 1)
    if (right && speed >= left.speed && speed <= right.speed) {
      return left.power + (right.power - left.power) * (speed - left.speed) / (right.speed - left.speed)
    }
  }
  return null
}

export default {
  watch: Object.values(files).map(file => '../../../public/data/' + file),
  load(paths) {
    const get = key => {
      const path = paths.find(path => path.endsWith(files[key]))
      if (!path) throw new Error('Missing teaching CSV: ' + files[key])
      return readRows(path)
    }
    const scada = get('scada')
    const lidar = get('lidar')
    const paired = get('paired')
    const firstMinutes = minutes.map(time => scada.find(r => r.time_utc.startsWith(windowDate + time)))
    const lidarRecord = lidar.find(r => r.time_center_utc.startsWith(windowDate + '00:05'))
    const eligible = paired.filter(r => r.eligible === 'True')
    const training = eligible.filter(r => r.window_start_utc < split)
    const heldOut = eligible.filter(r => r.window_start_utc >= split)
    const lidarCurve = powerCurve(training, 'lidar_ms')
    const nacelleCurve = powerCurve(training, 'nacelle_ms')
    const coverage = { both: 0, lidar: 0, nacelle: 0, neither: 0 }
    for (const row of heldOut) {
      const l = estimate(lidarCurve, num(row.lidar_ms)) !== null
      const n = estimate(nacelleCurve, num(row.nacelle_ms)) !== null
      coverage[l ? (n ? 'both' : 'lidar') : (n ? 'nacelle' : 'neither')]++
    }
    const comparison = ['lidar_ms', 'nacelle_ms'].map(source => {
      const summarize = rows => {
        const values = rows.filter(r => Math.floor(num(r[source])) === 6).map(r => num(r.power_kw))
        return { count: values.length, power: mean(values) }
      }
      return { source, before: summarize(training), after: summarize(heldOut) }
    })
    return {
      pairing: { minutes, nacelle: mean(firstMinutes.map(r => num(r.nacelle_ms))), lidar: num(lidarRecord.lidar_ms) },
      coverage: { ...coverage, total: heldOut.length },
      comparison
    }
  }
}
