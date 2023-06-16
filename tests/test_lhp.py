"""Asynchronous client for the Länderübergreifendes Hochwasserportal (LHP) API."""
# pylint: disable=protected-access
import asyncio

import aiohttp
import pytest
from yarl import URL

from lhp import LHP_client
from lhp.exceptions import LHPConnectionError, LHPError


@pytest.mark.asyncio
async def test_json_request(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        "example.com",
        "/api/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "text/html; charset=UTF-8"},
            text='{"status": "ok"}',
        ),
    )
    async with aiohttp.ClientSession() as session:
        lhp_client = LHP_client(session=session)
        response = await lhp_client._request(URL("http://example.com/api/"), {'pgnr': 'test'})
        assert response["status"] == "ok"


@pytest.mark.asyncio
async def test_internal_session(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        "example.com",
        "/api/",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "text/html; charset=UTF-8"},
            text='{"status": "ok"}',
        ),
    )
    async with LHP_client() as lhp_client:
        response = await lhp_client._request(URL("http://example.com/api/"), {'pgnr': 'test'})
        assert response["status"] == "ok"


@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        await asyncio.sleep(2)
        return aresponses.Response(body="Goodmorning!")

    aresponses.add("example.com", "/api/", "POST", response_handler)

    async with aiohttp.ClientSession() as session:
        lhp_client = LHP_client(
            session=session,
            request_timeout=1,
        )
        with pytest.raises(LHPConnectionError):
            assert await lhp_client._request(URL("http://example.com/api/"), {'pgnr': 'test'})


@pytest.mark.asyncio
async def test_http_error400(aresponses):
    """Test HTTP 404 response handling."""
    aresponses.add(
        "example.com",
        "/api/",
        "POST",
        aresponses.Response(text="OMG PUPPIES!", status=404),
    )

    async with aiohttp.ClientSession() as session:
        lhp_client = LHP_client(session=session)
        with pytest.raises(LHPError):
            assert await lhp_client._request(URL("http://example.com/api/"), {'pgnr': 'test'})


@pytest.mark.asyncio
async def test_http_error500(aresponses):
    """Test HTTP 500 response handling."""
    aresponses.add(
        "example.com",
        "/api/",
        "POST",
        aresponses.Response(
            body=b'{"status":"nok"}',
            status=500,
            headers={"Content-Type": "text/html; charset=UTF-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        lhp_client = LHP_client(session=session)
        with pytest.raises(LHPError):
            assert await lhp_client._request(URL("http://example.com/api/"), {'pgnr': 'test'})
