"""Test the HomeLINK property methods."""

from datetime import datetime

from pyhomelink.api import HomeLINKApi
from pyhomelink.insight import Insight

from .helpers.const import INSIGHT_ID, PROPERTY_REF
from .helpers.utils import create_mock


async def test_insights(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test insights request."""

    create_mock(mock_aio, "/insight", "insights.json")

    insights = await homelink_api.async_get_insights()

    assert len(insights) == 14
    insight = insights[0]
    assert isinstance(insight, Insight)
    assert insight.hl_type == "MOULD"
    assert insight.risklevel == "HIGH"
    assert insight.location == "HALLWAY1"
    assert isinstance(insight.calculatedat, datetime)
    assert insight.value == 93.3339
    assert insight.appliesto == "ROOM"
    assert insight.propertyreference == PROPERTY_REF
    assert insight.rel.self == f"insight/{insight.insightid}"
    assert insight.rel.hl_property == f"property/{PROPERTY_REF}"


async def test_insight(homelink_api: HomeLINKApi, mock_aio) -> None:
    """Test insights request."""

    create_mock(mock_aio, f"/insight/{INSIGHT_ID}", "insight.json")

    insight = await homelink_api.async_get_insight(INSIGHT_ID)

    assert insight.insightid == INSIGHT_ID
