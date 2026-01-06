from listy.analysis import extract_topics


async def test_english():
    text = "My neighbor Krzysztof's homemade pierogi are the best in our apartment building. Every Sunday, the smell wafts through the hallway and at least three families come knocking. His secret is adding a tiny bit of smoked cheese to the potato filling, which nobody else in the building does."
    result = await extract_topics(text)
    assert isinstance(result, list)
    assert len(result) > 0
    all_labels = " ".join(result).lower()
    assert any(
        keyword in all_labels
        for keyword in ["pierogi", "cheese", "sunday", "neighbor", "recipe", "cooking"]
    ), f"Expected relevant topics, got: {result}"


async def test_polish():
    text = "Pierogi mojego sąsiada Krzysztofa są najlepsze w całym bloku. W każdą niedzielę zapach unosi się po klatce schodowej i przynajmniej trzy rodziny pukają do jego drzwi. Jego sekret to dodanie odrobiny wędzonego sera do farszu ziemniaczanego, czego nikt inny w bloku nie robi."
    result = await extract_topics(text)
    assert isinstance(result, list)
    assert len(result) > 0
    all_labels = " ".join(result).lower()
    polish_indicators = [
        "pierogi",
        "ser",
        "sąsiad",
        "niedziela",
        "przepis",
        "gotowanie",
        "sekret",
    ]
    assert any(indicator in all_labels for indicator in polish_indicators), (
        f"Expected Polish topics, got: {result}"
    )
