@echo off
setlocal
cd /d "%~dp0" || exit /b 1

where node.exe >nul 2>&1
if errorlevel 1 (
    echo Install Node.js 22.13 or later, then reopen VS Code.
    exit /b 1
)
node -e "const [major, minor] = process.versions.node.split('.').map(Number); process.exit(major > 22 || (major === 22 && minor >= 13) ? 0 : 1)"
if errorlevel 1 (
    echo This project requires Node.js 22.13 or later. Current version:
    node --version
    exit /b 1
)

if exist "node_modules\vitepress\bin\vitepress.js" goto preview

echo Installing the tutorial dependencies...
where pnpm.cmd >nul 2>&1
if not errorlevel 1 (
    call pnpm.cmd install --frozen-lockfile
    goto check_install
)
where npx.cmd >nul 2>&1
if errorlevel 1 (
    echo Install Node.js with npm and npx, or make pnpm available on PATH.
    exit /b 1
)
for /f %%P in ('node -p "require('./package.json').packageManager"') do set "tutorial_pnpm=%%P"
call npx.cmd --yes %tutorial_pnpm% install --frozen-lockfile

:check_install
if errorlevel 1 exit /b 1
if not exist "node_modules\vitepress\bin\vitepress.js" (
    echo VitePress is missing after installation.
    exit /b 1
)

:preview
node ".\node_modules\vitepress\bin\vitepress.js" dev docs --host 127.0.0.1
exit /b %errorlevel%
