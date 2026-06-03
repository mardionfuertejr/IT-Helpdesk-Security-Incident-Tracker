# HelpDeskPro: IT Support & Security Incident Tracker

HelpDeskPro is a clean, responsive, and secure Django-based web application designed for corporate environments. It allows employees to submit IT support tickets and security incident reports, tracks ticket progress using simple workflows inspired by NIST incident response stages, and enables IT staff/managers and administrators to handle support requests efficiently.

---

## ── Table of Contents ──
1. [Key Features](#1-key-features)
2. [Technology Stack](#2-technology-stack)
3. [User Roles & Permissions](#3-user-roles--permissions)
4. [Workflows & NIST Stages](#4-workflows--nist-stages)
5. [Database Architecture & Models](#5-database-architecture--models)
6. [Security & Rate Limiting](#6-security--rate-limiting)
7. [Developer API Integration](#7-developer-api-integration)
8. [Installation & Setup](#8-installation--setup)
9. [Automated Testing](#9-automated-testing)
10. [Recent UI/UX & Mobile Responsiveness Improvements](#10-recent-uiux--mobile-responsiveness-improvements)

---

## 1. Key Features
*   **Centralized Dashboard**: Personalized metrics based on user roles (total, open, resolved, and closed tickets).
*   **Interactive Ticket Submission**: Guided form handling categories (Hardware, Software, Network, Account, Security) and priorities.
*   **NIST-Aligned Incident Tracking**: Visual timeline tracker mapping tickets to NIST Incident Response stages.
*   **Audit Logging**: Detailed database audit logs tracking status adjustments, profile edits, and user creations.
*   **API Integrations**: Fully functional REST APIs with JWT authentication for remote monitoring tools.
*   **UI Customization**: Supports Light & Dark theme modes (persisted in localStorage).

---

## 2. Technology Stack
*   **Backend Framework**: Django 6.0.5 (Python 3.13+)
*   **Database**: SQLite (local development) / PostgreSQL compatibility (configured via `dj_database_url`)
*   **API Framework**: Django REST Framework (DRF) + SimpleJWT for JWT Authentication
*   **Security Middleware**: Django-Axes (login protection) + Django-Ratelimit (view rate limiting)
*   **Frontend UI**: Vanilla CSS + Bootstrap 5.3 + FontAwesome 6.4 (Outfit/Inter Google Fonts)
*   **File Storage**: Cloudinary (integrated for ticket attachments & user avatars)

---

## 3. User Roles & Permissions
*   **Employee**: Can register, submit support requests and security incident reports, view/edit their own tickets while open, and update notification preferences.
*   **IT Manager (IT Staff)**: Can view all tickets, update ticket statuses, add resolution notes, and deactivate/activate users.
*   **Administrator**: Full access to all controls including manager tools, user management, and advanced system metrics.

---

## 4. Workflows & NIST Stages
Tickets are categorized into two types, each with its own simplified lifecycle:
*   **IT Support Ticket Workflow**: `Open` ➔ `In Progress` ➔ `Resolved` ➔ `Closed`
*   **Security Incident Workflow**: `Reported` ➔ `Investigating` ➔ `Fixed` ➔ `Closed`

Additionally, tickets are mapped to a visual stepper displaying the **NIST Incident Response Stages**:
1.  **Preparation** / **Open** (Initial logging)
2.  **Detection & Analysis / Containment** (Investigation by IT staff)
3.  **Eradication & Recovery** (Resolution applied)
4.  **Post-Incident Review / Closed** (Formal closure and archive)

---

## 5. Database Architecture & Models
The system consists of five main relational database models:
1.  **`CustomUser`**: Extends Django's `AbstractUser` with support for custom profile pictures, work departments, user roles (`employee`, `manager`), and notification toggles (`notify_tickets`, `notify_security`).
2.  **`Ticket`**: Represents support tickets or security incidents. It contains fields for description, status, priority, category, attachments, assignment, and tracking fields like `nist_stage`.
3.  **`TicketUpdate`**: Holds comments, progress updates, or resolution notes added to tickets by managers.
4.  **`LoginAttempt`**: Records successful and unsuccessful login attempts for security auditing.
5.  **`TicketLog`**: An audit trail record logging exact changes (e.g., status changes, field updates) made to tickets or user profiles.

---

## 6. Security & Rate Limiting

### Brute Force Login Protection (`django-axes`)
To protect against brute force login attacks, `django-axes` is integrated with the following custom security configurations:
*   **5-Minute Lockout**: The lockout cool-off period is set to 5 minutes (`AXES_COOLOFF_TIME = timedelta(minutes=5)`).
*   **Failure Limit**: Users/connections are locked out after 5 consecutive failed attempts (`AXES_FAILURE_LIMIT = 5`).
*   **IP-User Combination Lockout**: Configured to lock out the specific **combination of the username and IP address** (`AXES_LOCKOUT_PARAMETERS = [["ip_address", "username"]]`). This ensures that a brute-force attempt on a single account from one IP does not block other legitimate users logging in from the same office connection, loopback, or proxy.
*   **Proxy-Aware IP Resolution**: Utilizes a custom resolver `get_client_ip` to extract client IPs from header chains (like `HTTP_X_FORWARDED_FOR` behind Render load balancers), preventing the backend from accidentally locking out the reverse proxy's internal IP.

### Request Rate Limiting (`django-ratelimit`)
*   Protects form submissions (such as ticket creation) by limiting IP addresses to a maximum of **5 ticket creations per minute**.

---

## 7. Developer API Integration
HelpDeskPro exposes token-based API endpoints allowing external tools (like SIEMs, routers, or servers) to automatically report events.

### API Endpoints
*   `POST /api/token/` - Returns a JWT access token.
*   `POST /api/tickets/create/` - Submits an incident ticket (requires `Authorization: Bearer <Token>`).
*   `GET /api/tickets/` - Lists tickets for the authenticated user/manager.

### Access Token Generation
Users can generate a JWT token directly under **Settings ➔ Developer API Integration** to authorize external scripts.

### Curl Command Example
```bash
curl -X POST http://127.0.0.1:8000/api/tickets/create/ \
  -H "Authorization: Bearer YOUR_JWT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Suspicious DB Spikes",
    "description": "High volume database query load detected from unusual IP.",
    "ticket_type": "Security Incident",
    "priority": "High"
  }'
```

---

## 8. Installation & Setup

1.  **Clone the Repository** and navigate to the project root:
    ```bash
    git clone https://github.com/mardionfuertejr/IT-Helpdesk-Security-Incident-Tracker.git
    cd "IT Helpdesk & Security Incident Tracker"
    ```

2.  **Create and Activate Virtual Environment**:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    SECRET_KEY=your-django-secret-key-here
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    ```

5.  **Run Database Migrations**:
    ```bash
    python manage.py migrate
    ```

6.  **Seed Initial Database Data**:
    A built-in data seeder creates default users, sample tickets, and updates for testing:
    ```bash
    python setup_data.py
    ```
    *Seed Accounts created:*
    *   **IT Manager**: `manager@company.com` (password: `password123`)
    *   **Employee**: `employee@company.com` (password: `password123`)
    *   **Developer**: `dev@company.com` (password: `password123`)

7.  **Start Development Server**:
    ```bash
    python manage.py runserver
    ```
    Open `http://127.0.0.1:8000` in your web browser.

---

## 9. Automated Testing
Verify the backend, APIs, security settings, and lockout rules by running the Django unit tests:
```bash
python manage.py test
```

---

## 10. Recent UI/UX & Mobile Responsiveness Improvements
*   **Overlap Resolution**: Removed conflicting Bootstrap classes from the sidebar brand container. This lets the custom CSS top-padding of `85px` take effect on mobile screens, successfully shifting the "IT Helpdesk" logo below the floating hamburger close button (`menu-toggle`) to prevent overlaps.
*   **Recent Activity Polish**: Redesigned the activity list under [profile.html](file:///c:/Users/Dion/Desktop/IT%20Helpdesk%20&%20Security%20Incident%20Tracker/helpdesk/templates/helpdesk/profile.html) to dynamically stack into a vertical column on extra small screens and realign dates smoothly, ensuring readability on all mobile phone viewports.

# helpdesk-web
