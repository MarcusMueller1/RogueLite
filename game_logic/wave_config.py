# wave_config.py
from entities.enemy_types import FastEnemy, TankEnemy

wave_data = [
    {
        "enemy_configs": [(FastEnemy, 5, 'fast_enemy.png', 4), (TankEnemy, 3, 'tank_enemy.png', 1)],
        "spawn_delay": 800
    },
    {
        "enemy_configs": [(TankEnemy, 2, 'tank_enemy.png', 1), (FastEnemy, 4, 'fast_enemy.png', 4)],
        "spawn_delay": 1000
    },
    # Add more waves here
]
