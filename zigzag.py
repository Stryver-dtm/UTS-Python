import time, sys, random, json
from datetime import datetime

indent = 0
indentIncreasing = True
wave_count = 0
game_data = {
    'level': 1,
    'score': 0,
    'player_name': 'Wave Explorer',
    'inventory': [],
    'boss_defeated': False
}
quests = [
    "Kumpulkan 5 Energy Crystal",
    "Kalahkan Boss Gelombang", 
    "Capai Level 5",
    "Kumpulkan 10 Poin Score"
]

def mini_game_event():
    """Fitur 1: Mini Game yang muncul acak selama gelombang berjalan"""
    if random.random() < 0.15 and wave_count > 0:  # 15% chance muncul game
        games = [
            "🎯 TEBAK ANGKA",
            "🎲 ROULETTE", 
            "🪨 BATU-GUNTING-KERTAS",
            "🧮 MATH CHALLENGE"
        ]
        chosen_game = random.choice(games)
        
        print(f"\n🎮 [MINI GAME: {chosen_game}]")
        
        if chosen_game == "🎯 TEBAK ANGJA":
            return number_guessing_game()
        elif chosen_game == "🎲 ROULETTE":
            return roulette_game()
        elif chosen_game == "🪨 BATU-GUNTING-KERTAS":
            return rps_game()
        else:
            return math_challenge()
    
    return None

def number_guessing_game():
    """Game tebak angka sederhana"""
    target = random.randint(1, 5)
    print("Tebak angka 1-5: ", end="")
    
    try:
        guess = int(sys.stdin.readline().strip())
        if guess == target:
            reward = random.randint(10, 25)
            game_data['score'] += reward
            print(f"🎉 Benar! +{reward} Score!")
            return True
        else:
            print(f"❌ Salah! Angkanya: {target}")
            return False
    except:
        print("❌ Input tidak valid!")
        return False

def roulette_game():
    """Game roulette sederhana"""
    options = ['MERAH', 'HITAM', 'HIJAU']
    bet = random.choice(options)
    result = random.choice(options)
    
    print(f"Taruhanmu: {bet}")
    print(f"Hasil: {result}")
    
    if bet == result:
        reward = 30 if result == 'HIJAU' else 15
        game_data['score'] += reward
        print(f"🎉 Menang! +{reward} Score!")
        return True
    else:
        print("💸 Coba lagi!")
        return False

def rps_game():
    """Game batu-gunting-kertas"""
    choices = ['🪨 BATU', '✂️ GUNTING', '📄 KERTAS']
    computer = random.choice(choices)
    
    print("Pilih: 1=🪨 2=✂️ 3=📄: ", end="")
    try:
        player_choice = int(sys.stdin.readline().strip()) - 1
        if 0 <= player_choice <= 2:
            player = choices[player_choice]
            print(f"Kamu: {player} vs Computer: {computer}")
            
            if player == computer:
                print("🤝 Seri! +5 Score")
                game_data['score'] += 5
                return True
            elif (player == "🪨 BATU" and computer == "✂️ GUNTING") or \
                 (player == "✂️ GUNTING" and computer == "📄 KERTAS") or \
                 (player == "📄 KERTAS" and computer == "🪨 BATU"):
                game_data['score'] += 20
                print(f"🎉 Menang! +20 Score!")
                return True
            else:
                print("❌ Kalah!")
                return False
    except:
        print("❌ Input tidak valid!")
    
    return False

def math_challenge():
    """Challenge matematika cepat"""
    a, b = random.randint(1, 10), random.randint(1, 10)
    operations = ['+', '-', '*']
    op = random.choice(operations)
    
    if op == '+':
        answer = a + b
    elif op == '-':
        answer = a - b
    else:
        answer = a * b
    
    print(f"Berapa {a} {op} {b}? ", end="")
    
    try:
        user_answer = int(sys.stdin.readline().strip())
        if user_answer == answer:
            reward = 25
            game_data['score'] += reward
            print(f"🎉 Benar! +{reward} Score!")
            return True
        else:
            print(f"❌ Salah! Jawabannya: {answer}")
            return False
    except:
        print("❌ Input tidak valid!")
        return False

def achievement_system():
    """Fitur 2: Sistem Achievement/Pencapaian"""
    achievements = []
    
    # Check achievements
    if game_data['score'] >= 50 and 'SCORE_MASTER' not in game_data['inventory']:
        achievements.append("🏆 SCORE MASTER (50+ Points)")
        game_data['inventory'].append('SCORE_MASTER')
    
    if wave_count >= 10 and 'WAVE_EXPLORER' not in game_data['inventory']:
        achievements.append("🌊 WAVE EXPLORER (10+ Waves)")
        game_data['inventory'].append('WAVE_EXPLORER')
    
    if len([x for x in game_data['inventory'] if 'SCORE' in x or 'WAVE' in x]) >= 3:
        if 'COLLECTOR' not in game_data['inventory']:
            achievements.append("🎯 ACHIEVEMENT COLLECTOR (3+ Achievements)")
            game_data['inventory'].append('COLLECTOR')
    
    if wave_count >= 20 and 'LEGEND' not in game_data['inventory']:
        achievements.append("👑 LEGENDARY WALKER (20+ Waves)")
        game_data['inventory'].append('LEGEND')
    
    # Level up system
    new_level = min(game_data['score'] // 25 + 1, 10)
    if new_level > game_data['level']:
        old_level = game_data['level']
        game_data['level'] = new_level
        print(f"\n✨ LEVEL UP! {old_level} → {new_level}!")
        if new_level == 5:
            achievements.append("🚀 SPEED DEMON (Level 5)")
            game_data['inventory'].append('SPEED_DEMON')
    
    # Display achievements
    if achievements:
        print("\n🎉 ACHIEVEMENT UNLOCKED!")
        for achievement in achievements:
            print(f"   ✅ {achievement}")

def save_game_state():
    """Auto-save game state"""
    if wave_count % 5 == 0 and wave_count > 0:
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'wave_count': wave_count,
            'game_data': game_data,
            'total_play_time': wave_count * 0.1
        }
        print(f"💾 Auto-saved at wave {wave_count}")

def display_game_status():
    """Menampilkan status game"""
    if wave_count % 3 == 0 or random.random() < 0.2:
        print(f"\n📊 [STATUS] Level: {game_data['level']} | Score: {game_data['score']} | Waves: {wave_count}")
        print(f"🎒 Inventory: {', '.join(game_data['inventory']) if game_data['inventory'] else 'Empty'}")

def special_events():
    """Event spesial berdasarkan kondisi tertentu"""
    # Boss battle every 15 waves
    if wave_count % 15 == 0 and wave_count > 0 and not game_data['boss_defeated']:
        print(f"\n🐉 BOSS BATTLE! Wave {wave_count}")
        print("⚔️ Serang Boss dengan mengetik 'ATTACK': ", end="")
        try:
            attack = sys.stdin.readline().strip().upper()
            if attack == 'ATTACK':
                if random.random() < 0.7:  # 70% chance menang
                    game_data['score'] += 100
                    game_data['boss_defeated'] = True
                    print("🎉 BOSS DEFEATED! +100 Score!")
                    return True
                else:
                    print("💥 Boss menyerang balik! Coba lagi di wave berikutnya.")
            else:
                print("❌ Serangan gagal!")
        except:
            print("❌ Input tidak valid!")
    
    return False

try:
    print("🎮 WAVE ADVENTURE GAME STARTED!")
    print("💡 Mini games akan muncul secara acak selama perjalanan!")
    print("🏆 Kumpulkan achievement dan level up!\n")
    
    while True:
        # Main wave pattern (tetap jalan di background)
        print(' ' * indent, end='')
        print('~' * 8)
        time.sleep(0.1)

        # Game features
        mini_game_event()
        achievement_system()
        save_game_state()
        display_game_status()
        special_events()

        # Original wave logic
        if indentIncreasing:
            indent = indent + 1
            if indent == 20:
                indentIncreasing = False
        else:
            indent = indent - 1
            if indent == 0:
                indentIncreasing = True
                wave_count += 1

except KeyboardInterrupt:
    print(f"\n\n🎮 GAME OVER - FINAL STATS")
    print(f"📈 Total Waves: {wave_count}")
    print(f"⭐ Final Level: {game_data['level']}")
    print(f"🏅 Final Score: {game_data['score']}")
    print(f"🎖️  Achievements: {len(game_data['inventory'])}")
    print(f"📜 Inventory: {', '.join(game_data['inventory'])}")
    print("👏 Terima kasih sudah bermain!")
    sys.exit()