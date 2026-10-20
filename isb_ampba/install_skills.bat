@echo off
REM Copies AMPBA skills into .claude\skills (double-click or run from this folder)
if not exist "%~dp0.claude\skills" mkdir "%~dp0.claude\skills"
xcopy "%~dp0claude-skills\*" "%~dp0.claude\skills\" /E /I /Y
echo Done. Skills installed in .claude\skills
pause
