# From Vulnerable to Secure

A practical analysis of the OWASP Top 10:2025 for COMP6841 Security Engineering.

## Project Goal

This project investigates how common web application vulnerabilities occur and how secure development controls can prevent them.

## Practical Scope

The project develops a small local Flask application containing vulnerable and secure implementations of:

- A01:2025 Broken Access Control - IDOR
- A05:2025 Injection - Stored XSS
- A07:2025 Authentication Failures - account enumeration and unlimited login attempts

## Method

Each experiment includes:

1. A vulnerable implementation
2. A controlled local attack
3. A secure implementation
4. Tests comparing the results
5. Analysis of the cause, impact, mitigation, and limitations

## Ethical Boundary

This application is intentionally vulnerable and must only be run in a local testing environment. It is not designed for deployment or for testing systems without permission.