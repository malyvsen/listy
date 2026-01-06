from listy.analysis import extract_main_argument


async def test_english():
    text = "My neighbor Krzysztof's homemade pierogi are the best in our apartment building. Every Sunday, the smell wafts through the hallway and at least three families come knocking. His secret is adding a tiny bit of smoked cheese to the potato filling, which nobody else in the building does."
    result = await extract_main_argument(text)
    assert "krzysztof" in result.lower()
    assert "pierogi" in result.lower()


async def test_polish():
    text = "Pierogi mojego sąsiada Krzysztofa są najlepsze w całym bloku. W każdą niedzielę zapach unosi się po klatce schodowej i przynajmniej trzy rodziny pukają do jego drzwi. Jego sekret to dodanie odrobiny wędzonego sera do farszu ziemniaczanego, czego nikt inny w bloku nie robi."
    result = await extract_main_argument(text)
    assert "krzysztof" in result.lower()
    assert "pierogi" in result.lower()
    polish_indicators = [
        "są",
        "najlepsze",
        "sąsiada",
        "jego",
        "ser",
        "ziemniaczan",
        "farsz",
    ]
    assert any(
        indicator in result.lower() for indicator in polish_indicators
    ), f"Expected Polish response, got: {result}"
