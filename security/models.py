from django.db import models


class SecurityResult(models.Model):

    TEST_CHOICES = [
        ("SQL Injection", "SQL Injection"),
        ("XSS", "Cross Site Scripting"),
        ("CSRF", "CSRF Protection"),
        ("Authentication", "Authentication Check"),
    ]

    STATUS_CHOICES = [
        ("Passed", "Passed"),
        ("Failed", "Failed"),
    ]

    SEVERITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    test_name = models.CharField(
        max_length=50,
        choices=TEST_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES
    )

    description = models.TextField()

    recommendation = models.TextField()

    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name} - {self.status}"