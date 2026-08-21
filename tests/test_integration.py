import pytest

from raavone_router import (
    ExecutionResult,
    RaavOneRouter,
    RouteType,
)


class FakeExecutor:

    def execute(self, route):
        return ExecutionResult(
            success=True,
            result=f"executed:{route.target}",
            route=route,
        )

    async def aexecute(self, route):
        return self.execute(route)

    def execute_all(self, routing):
        return [
            self.execute(route)
            for route in routing.routes
        ]

    async def aexecute_all(self, routing):
        results = []

        for route in routing.routes:
            results.append(
                await self.aexecute(route)
            )

        return results


def test_end_to_end_single_route():

    router = RaavOneRouter()
    executor = FakeExecutor()

    routing = router.route_all(
        "What is the weather today?"
    )

    results = executor.execute_all(routing)

    assert len(results) == 1

    assert results[0].success is True
    assert results[0].route.type == RouteType.TOOL
    assert results[0].route.target == "weather"

    assert results[0].result == "executed:weather"


def test_end_to_end_multi_route():

    router = RaavOneRouter()
    executor = FakeExecutor()

    routing = router.route_all(
        "Remember my name and search the weather"
    )

    results = executor.execute_all(routing)

    assert len(results) == 2

    assert results[0].route.type == RouteType.MEMORY
    assert results[0].route.target == "memory"

    assert results[1].route.type == RouteType.TOOL
    assert results[1].route.target == "weather"


@pytest.mark.asyncio
async def test_end_to_end_async():

    router = RaavOneRouter()
    executor = FakeExecutor()

    routing = await router.aroute_all(
        "Remember my name and search the weather"
    )

    results = await executor.aexecute_all(routing)

    assert len(results) == 2

    assert all(
        result.success
        for result in results
    )

    assert results[0].route.target == "memory"
    assert results[1].route.target == "weather"