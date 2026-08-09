import json

def test_spells_validity():
    with open("spell_list.json", "r") as f:
        spells = json.load(f)

        spell = spells[0]
        assert "name" in spell
        assert "source" in spell
        assert "type" in spell
        assert "casting_time" in spell
        assert "range" in spell
        assert "components" in spell
        assert "duration" in spell
        assert "description" in spell

def test_spells_count():
    with open("spell_list.json", "r") as f:
        spells = json.load(f)

        assert len(spells) > 0