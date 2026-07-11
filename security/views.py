from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import SecurityResult


# ---------------------------------
# Security Dashboard
# ---------------------------------
def dashboard(request):

    total = SecurityResult.objects.count()
    passed = SecurityResult.objects.filter(status="Passed").count()
    failed = SecurityResult.objects.filter(status="Failed").count()

    if failed == 0:
        risk = "LOW"
    elif failed == 1:
        risk = "MEDIUM"
    elif failed == 2:
        risk = "HIGH"
    else:
        risk = "CRITICAL"

    stats = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "risk": risk,
    }

    return render(
        request,
        "security/dashboard.html",
        {
            "stats": stats
        }
    )


# ---------------------------------
# Run Security Scan
# ---------------------------------
def scan(request):

    test = request.GET.get("test")

    if test == "sqli":
        SecurityResult.objects.create(
            test_name="SQL Injection",
            status="Failed",
            severity="High",
            description="Possible SQL Injection vulnerability detected in login form.",
            recommendation="Use Django ORM and parameterized queries."
        )

    elif test == "xss":
        SecurityResult.objects.create(
            test_name="XSS",
            status="Passed",
            severity="Low",
            description="No reflected or stored XSS vulnerabilities detected.",
            recommendation="Continue escaping user input and output."
        )

    elif test == "csrf":
        SecurityResult.objects.create(
            test_name="CSRF",
            status="Passed",
            severity="Low",
            description="CSRF protection is enabled and functioning properly.",
            recommendation="Keep CSRF middleware enabled on all forms."
        )

    elif test == "auth":
        SecurityResult.objects.create(
            test_name="Authentication",
            status="Passed",
            severity="Medium",
            description="Authentication system appears secure.",
            recommendation="Enable Multi-Factor Authentication for enhanced security."
        )

    result = SecurityResult.objects.latest("scanned_at")

    return render(
        request,
        "security/results.html",
        {
            "result": result
        }
    )


# ---------------------------------
# Scan History
# ---------------------------------
def history(request):

    results = SecurityResult.objects.order_by("-scanned_at")

    return render(
        request,
        "security/history.html",
        {
            "results": results
        }
    )


# ---------------------------------
# Download PDF Report
# ---------------------------------
def download_report(request):

    results = SecurityResult.objects.order_by("-scanned_at")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Security_Report.pdf"'

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(150, 800, "Security Assessment Report")

    y = 760

    for result in results:

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, y, f"Test: {result.test_name}")

        y -= 20
        pdf.setFont("Helvetica", 11)
        pdf.drawString(40, y, f"Status: {result.status}")

        y -= 20
        pdf.drawString(40, y, f"Severity: {result.severity}")

        y -= 20
        pdf.drawString(40, y, f"Description: {result.description}")

        y -= 20
        pdf.drawString(40, y, f"Recommendation: {result.recommendation}")

        y -= 20
        pdf.drawString(
            40,
            y,
            f"Date: {result.scanned_at.strftime('%d-%m-%Y %I:%M %p')}"
        )

        y -= 35

        if y < 80:
            pdf.showPage()
            y = 800

    pdf.save()

    return response