FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# 1. Копируем ЛЮБОЙ найденный .csproj файл и восстанавливаем зависимости
COPY *.csproj ./
RUN dotnet restore

# 2. Копируем весь остальной исходный код
COPY . .

# 3. Публикуем приложение (dotnet сам найдет проект)
RUN dotnet publish -c Release -o /app/publish /p:UseAppHost=false

# --- Runtime stage ---
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
EXPOSE 8080

COPY --from=build /app/publish .

ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Development

# 4. Умный запуск: находим главный .dll файл (игнорируя системные библиотеки)
ENTRYPOINT ["sh", "-c", "dotnet $(ls *.dll | grep -vE '^(Microsoft|System|netstandard|Azure|Newtonsoft)' | head -n 1)"]