namespace Client.Models
{
    public class ReportTask
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        public string UserId { get; set; } = string.Empty; // Пока хардкодим, потом добавишь Auth
        public string OriginalFileName { get; set; } = string.Empty;
        public string InputFilePath { get; set; } = string.Empty;
        public string? ResultFilePath { get; set; }

        // Pending, Processing, Ready, Failed
        public string Status { get; set; } = "Pending";
        public string? ErrorMessage { get; set; }

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public DateTime? UpdatedAt { get; set; }
    }
}
