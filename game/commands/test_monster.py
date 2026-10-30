from game.engine import Monster, Item

monster = Monster(name="Goblin", hp=25, max_hp=50, dmg=10)
monster.take(Item(name="Gold Coin", description="A shiny gold coin."))
print(monster.inventory)
monster.damage(10)
print(monster.hp)  # Should print 15 
monster.heal(20)
print(monster.hp)  # Should print 35, but not exceed max_hp (50
print(monster.drop("Gold Coin"))
print(monster.inventory)  # Should print an empty list after dropping the item