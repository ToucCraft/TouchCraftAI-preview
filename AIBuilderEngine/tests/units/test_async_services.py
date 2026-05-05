import pytest
from unittest.mock import patch, AsyncMock
from services.email_sender import send_lead_email
from services.notifier import send_activation_link


@pytest.mark.asyncio
@patch('services.email_sender.aiosmtplib.send', new_callable=AsyncMock)
async def test_send_lead_email_success(mock_smtp_send):
    """
    Test: Verify that the lead notification email is dispatched via SMTP asynchronously.
    """
    smtp_config = {
        "host": "smtp.test.com",
        "port": 587,
        "username": "user",
        "password": "pwd",
        "from_email": "leads@test.com"
    }
    lead_data = {"name": "John Doe", "phone": "123456789"}

    await send_lead_email(smtp_config, "owner@test.com", lead_data, "Test Project")

    # Assert that aiosmtplib.send was awaited
    mock_smtp_send.assert_awaited_once()


@pytest.mark.asyncio
@patch('services.notifier.aiosmtplib.send', new_callable=AsyncMock)
async def test_send_activation_link(mock_smtp_send):
    """
    Test: Verify that the activation link email is sent to the admin.
    """
    await send_activation_link("user-uuid-123", "newuser@test.com")

    mock_smtp_send.assert_awaited_once()
