premake4.exe --only-shared --only-double --platform=x64 vs2010
cd vs2010
msbuild.exe ode.vcxproj /p:PlatformToolset=v140 /p:PreferredToolArchitecture=x64 /p:Configuration=Release
cd ..
