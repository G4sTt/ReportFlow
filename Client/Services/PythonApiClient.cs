using System.Text;
using System.Text.Json;

namespace Client.Services
{
    public interface IPythonApiClient
    {
        Task<bool> SendTaskToProcessingAsync(Guid taskId, string inputFilePath);
    }
    public class PythonApiClient : IPythonApiClient
    {
        private readonly HttpClient _httpClient;
        private readonly IConfiguration _configuration;

        public PythonApiClient(HttpClient httpClient, IConfiguration configuration)
        {
            _httpClient = httpClient;
            _configuration = configuration;
        }

        public async Task<bool> SendTaskToProcessingAsync(Guid taskId, string inputFilePath)
        {
            var pythonUrl = _configuration["PythonApi:BaseUrl"];
            // Ожидаем, что в Python будет эндпоинт POST /process
            var requestUrl = $"{pythonUrl}/process";

            var payload = new
            {
                taskId = taskId.ToString(),
                inputPath = inputFilePath
            };

            var json = JsonSerializer.Serialize(payload);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            try
            {
                var response = await _httpClient.PostAsync(requestUrl, content);
                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                // Тут нужно логировать ошибку
                Console.WriteLine($"Error calling Python API: {ex.Message}");
                return false;
            }
        }
    }
}
