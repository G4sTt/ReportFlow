using Client.Data;
using Client.Models;
using Client.Services;
using Microsoft.AspNetCore.Mvc;

namespace Client.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TasksController : ControllerBase
    {
        private readonly AppDbContext _db;
        private readonly IPythonApiClient _pythonClient;
        private readonly IConfiguration _config;

        public TasksController(AppDbContext db, IPythonApiClient pythonClient, IConfiguration config)
        {
            _db = db;
            _pythonClient = pythonClient;
            _config = config;
        }

        // 1. Клиент загружает файл
        [HttpPost("upload")]
        public async Task<IActionResult> Upload(IFormFile file)
        {
            if (file == null || file.Length == 0)
                return BadRequest("No file provided");

            var taskId = Guid.NewGuid();

            // Пути внутри контейнера (они должны быть замаунчены в docker-compose)
            var uploadDir = _config["SharedPaths:Uploads"] ?? "/shared/uploads";
            Directory.CreateDirectory(uploadDir);

            var inputFilePath = Path.Combine(uploadDir, $"{taskId}.csv");

            // 1. Сохраняем файл на диск
            using (var stream = new FileStream(inputFilePath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }

            // 2. Создаем запись в БД
            var task = new ReportTask
            {
                Id = taskId,
                UserId = "default_user", // Потом заменим на User.Identity.Name
                OriginalFileName = file.FileName,
                InputFilePath = inputFilePath,
                Status = "Processing"
            };

            _db.ReportTasks.Add(task);
            await _db.SaveChangesAsync();

            // 3. Отправляем задачу в Python
            var sent = await _pythonClient.SendTaskToProcessingAsync(taskId, inputFilePath);

            if (!sent)
            {
                task.Status = "Failed";
                task.ErrorMessage = "Failed to contact Python API";
                await _db.SaveChangesAsync();
                return StatusCode(500, "Processing service unavailable");
            }

            return Ok(new { taskId = task.Id, status = task.Status });
        }

        // 2. Клиент проверяет статус
        [HttpGet("{id}")]
        public async Task<IActionResult> GetStatus(Guid id)
        {
            var task = await _db.ReportTasks.FindAsync(id);
            if (task == null) return NotFound();

            return Ok(new
            {
                id = task.Id,
                status = task.Status,
                originalFileName = task.OriginalFileName,
                errorMessage = task.ErrorMessage,
                createdAt = task.CreatedAt
            });
        }

        // 3. Клиент скачивает готовый PDF
        [HttpGet("{id}/download")]
        public async Task<IActionResult> Download(Guid id)
        {
            var task = await _db.ReportTasks.FindAsync(id);
            if (task == null) return NotFound();

            if (task.Status != "Ready")
                return BadRequest($"Task is not ready. Current status: {task.Status}");

            if (task.ResultFilePath == null || !System.IO.File.Exists(task.ResultFilePath))
                return NotFound("Result file not found on disk");

            // Читаем файл и отдаем клиенту
            var fileBytes = await System.IO.File.ReadAllBytesAsync(task.ResultFilePath);
            var fileName = $"Report_{task.OriginalFileName.Replace(".csv", "")}.pdf";

            return File(fileBytes, "application/pdf", fileName);
        }
    }
}
