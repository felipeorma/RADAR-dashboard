
# metrics_config.py

summarized_metrics = {
    'Goalkeeper': {
        'es': {
            'Prevención': {
                'Save rate, %': 0.4,
                'Prevented goals per 90': 0.3,
                'Conceded goals per 90': -0.3
            },
            'Distribución': {
                'Accurate forward passes, %': 0.5,
                'Accurate long passes, %': 0.5
            },
            'Juego con Balón': {
                'Received passes per 90': 0.3,
                'Accurate lateral passes, %': 0.3,
                'Accurate forward passes, %': 0.4
            },
            'Movimiento': {
                'Aerial duels per 90': 0.6,
                'Exits per 90': 0.4
            },
            'Posicionamiento': {
                'xG against per 90': -0.6,
                'Exits per 90': 0.4
            }
        },
        'en': {
            'Prevention': {
                'Save rate, %': 0.4,
                'Prevented goals per 90': 0.3,
                'Conceded goals per 90': -0.3
            },
            'Distribution': {
                'Accurate forward passes, %': 0.5,
                'Accurate long passes, %': 0.5
            },
            'Ball Playing': {
                'Received passes per 90': 0.3,
                'Accurate lateral passes, %': 0.3,
                'Accurate forward passes, %': 0.4
            },
            'Movement': {
                'Aerial duels per 90': 0.6,
                'Exits per 90': 0.4
            },
            'Positioning': {
                'xG against per 90': -0.6,
                'Exits per 90': 0.4
            }
        }
    },
    'Defender': {
        'es': {
            'Ataque': {
                'Progressive runs per 90': 0.5,
                'Accelerations per 90': 0.5
            },
            'Construcción': {
                'Accurate passes, %': 0.6,
                'Accurate long passes, %': 0.4
            },
            'Progresión': {
                'Progressive runs per 90': 0.5,
                'Accelerations per 90': 0.5
            },
            'Defensa': {
                'Defensive duels won, %': 0.4,
                'Sliding tackles per 90': 0.3,
                'Interceptions per 90': 0.3
            },
            'Posicionamiento': {
                'Interceptions per 90': 0.6,
                'Defensive duels won, %': 0.4
            }
        },
        'en': {
            'Attack': {
                'Progressive runs per 90': 0.5,
                'Accelerations per 90': 0.5
            },
            'Build-up': {
                'Accurate passes, %': 0.6,
                'Accurate long passes, %': 0.4
            },
            'Progression': {
                'Progressive runs per 90': 0.5,
                'Accelerations per 90': 0.5
            },
            'Defense': {
                'Defensive duels won, %': 0.4,
                'Sliding tackles per 90': 0.3,
                'Interceptions per 90': 0.3
            },
            'Positioning': {
                'Interceptions per 90': 0.6,
                'Defensive duels won, %': 0.4
            }
        }
    },
    'Fullback': {
        'es': {
            'Ataque': {
                'Successful attacking actions per 90': 0.4,
                'Crosses to goalie box per 90': 0.3,
                'Offensive duels won, %': 0.3
            },
            'Construcción': {
                'Accurate through passes, %': 0.4,
                'Passes per 90': 0.3,
                'Received passes per 90': 0.3
            },
            'Progresión': {
                'xA per 90': 0.6,
                'Accurate through passes, %': 0.4
            },
            'Movimiento': {
                'Accelerations per 90': 0.5,
                'Progressive runs per 90': 0.5
            },
            'Defensa': {
                'Defensive duels won, %': 0.6,
                'Interceptions per 90': 0.4
            }
        },
        'en': {
            'Attack': {
                'Successful attacking actions per 90': 0.4,
                'Crosses to goalie box per 90': 0.3,
                'Offensive duels won, %': 0.3
            },
            'Build-up': {
                'Accurate through passes, %': 0.4,
                'Passes per 90': 0.3,
                'Received passes per 90': 0.3
            },
            'Progression': {
                'xA per 90': 0.6,
                'Accurate through passes, %': 0.4
            },
            'Movement': {
                'Accelerations per 90': 0.5,
                'Progressive runs per 90': 0.5
            },
            'Defense': {
                'Defensive duels won, %': 0.6,
                'Interceptions per 90': 0.4
            }
        }
    },
    'Midfielder': {
        'es': {
            'Ataque': {
                'xG per 90': 0.5,
                'Goals per 90': 0.5
            },
            'Construcción': {
                'Received passes per 90': 0.4,
                'Accurate short / medium passes, %': 0.6
            },
            'Progresión': {
                'Successful dribbles, %': 0.4,
                'Accurate short / medium passes, %': 0.3,
                'Accurate passes to final third, %': 0.3
            },
            'Creación': {
                'Assists per 90': 0.5,
                'xA per 90': 0.5
            },
            'Defensa': {
                'Defensive duels won, %': 0.5,
                'Interceptions per 90': 0.5
            }
        },
        'en': {
            'Attack': {
                'xG per 90': 0.5,
                'Goals per 90': 0.5
            },
            'Build-up': {
                'Received passes per 90': 0.4,
                'Accurate short / medium passes, %': 0.6
            },
            'Progression': {
                'Successful dribbles, %': 0.4,
                'Accurate short / medium passes, %': 0.3,
                'Accurate passes to final third, %': 0.3
            },
            'Creation': {
                'Assists per 90': 0.5,
                'xA per 90': 0.5
            },
            'Defense': {
                'Defensive duels won, %': 0.5,
                'Interceptions per 90': 0.5
            }
        }
    },
    'Wingers': {
        'es': {
            'Ataque': {
                'xG per 90': 0.4,
                'Goals per 90': 0.4,
                'Touches in box per 90': 0.2
            },
            'Construcción': {
                'Accurate passes to final third, %': 1.0
            },
            'Progresión': {
                'Offensive duels won, %': 0.5,
                'Successful dribbles, %': 0.5
            },
            'Creación': {
                'xA per 90': 0.4,
                'Assists per 90': 0.4,
                'Accurate passes to final third, %': 0.2
            },
            'Defensa': {
                'Defensive duels won, %': 0.6,
                'Interceptions per 90': 0.4
            }
        },
        'en': {
            'Attack': {
                'xG per 90': 0.4,
                'Goals per 90': 0.4,
                'Touches in box per 90': 0.2
            },
            'Build-up': {
                'Accurate passes to final third, %': 1.0
            },
            'Progression': {
                'Offensive duels won, %': 0.5,
                'Successful dribbles, %': 0.5
            },
            'Creation': {
                'xA per 90': 0.4,
                'Assists per 90': 0.4,
                'Accurate passes to final third, %': 0.2
            },
            'Defense': {
                'Defensive duels won, %': 0.6,
                'Interceptions per 90': 0.4
            }
        }
    },
    'Forward': {
        'es': {
            'Ataque': {
                'xG per 90': 0.3,
                'Goals per 90': 0.4,
                'Non-penalty goals per 90': 0.3
            },
            'Construcción': {
                'Passes to penalty area per 90': 0.5,
                'Accurate passes to final third, %': 0.5
            },
            'Progresión': {
                'Head goals per 90': 0.5,
                'Aerial duels won, %': 0.5
            },
            'Creación': {
                'xA per 90': 0.5,
                'Assists per 90': 0.5
            },
            'Movimiento': {
                'Touches in box per 90': 0.6,
                'Passes to penalty area per 90': 0.4
            }
        },
        'en': {
            'Attack': {
                'xG per 90': 0.3,
                'Goals per 90': 0.4,
                'Non-penalty goals per 90': 0.3
            },
            'Build-up': {
                'Passes to penalty area per 90': 0.5,
                'Accurate passes to final third, %': 0.5
            },
            'Progression': {
                'Head goals per 90': 0.5,
                'Aerial duels won, %': 0.5
            },
            'Creation': {
                'xA per 90': 0.5,
                'Assists per 90': 0.5
            },
            'Movement': {
                'Touches in box per 90': 0.6,
                'Passes to penalty area per 90': 0.4
            }
        }
    }
}
