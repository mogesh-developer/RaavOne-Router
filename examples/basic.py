from raavone_router import RaavOneRouter


router = RaavOneRouter()

messages = [
    "Explain Python decorators",
    "What did I say in my previous conversation?",
    "What's the weather today?",
]

for message in messages:
    result = router.route(message)

    print(f"\nMessage : {message}")
    print(f"Type    : {result.type.value}")
    print(f"Target  : {result.target}")
    print(f"Score   : {result.confidence}")