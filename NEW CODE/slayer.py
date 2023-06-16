import time
import sys
import random

player_name = ''
player_lvl = 0
player_class = 0 #Class to be chosen at the start
class_list = ['Mage', 'Archer', 'Warrior', 'Paladin'] #List of class options
health = 10 #Base health stat
spec = 5 #Base spec stat
spec_list = ['Mana', 'Stamina', 'Strength', 'Prayer'] #Class-specific names for spec
food = 3 #Starting food
tier0 = True
tier0_list = ['Runes', 'Shortbow', 'Dagger', 'Amulet'] #Starting equipment
tier1 = False
tier1_list = ['Wand', 'Longbow', 'Sword', 'Mace'] #First set of upgrades (offense)
tier2 = False
tier2_list = ['Robes', 'Leathers', 'Armour', 'Holy Book'] #Second set of upgrades (defense)
tier3 = False
tier3_list = ['Staff', 'Crossbow', 'Battleaxe', 'Warhammer'] #Third set of upgrades (offense)
boss_list = ['Rat', 'Bear', 'Dragon', 'Necromancer', 'Narrator']
boss_health = [5, 10, 20, 30, 50]

# carriage location 
village_loc = set([ "village", "1" ])
cave_loc = set([ "cave", "2" ])
forest_loc = set([ "forest", "3" ]) 
swamp_loc = set([ "witch", "swamp", "sherk", "4" ])
mountain_loc = set([ "mountain", "dragon", "5" ])
necro_loc = set([ "necromancer", "tower", "6", "necromancers" ])

carriage_loc = set([ "jimmy", "3", "carriage", "fast", "travel" ])

shop_loc = set([ "shop", "1" ]) 
tavern_loc = set([ "tavern", "2" ]) 

look_around = set([ "look", "around", "1", "investigate" ])

enter_cave = set([ "enter", "cave", "2"])

enter_dralair = set([ "enter", "lair", "2"])

enter_nectow = set([ "enter", "tower", "2"])

# confrontation options.
fight = set([ "1", "Fight" ])
run = set([ "run", "2", "escape", "retreat" ])

investigate = set([ "investigate" ])#
loc_info = set([ "information", "location" ])

witches_secret = 0

# Forest options.
human = ( "human footprints" )
bear = ( "bear tracks" )
foot_prints = ( "[ 2. Follow the foot prints.                ]" )
bear_tracks = ( "[ 2. Follow the tracks.                     ]" )
follow_tracks = set([ "bear", "tracks", "2"])
follow_prints = set([ "foot", "prints", "2" ])

jimmy_greeted = 0 # Jimmy greeted by the player is 1.

crash = False # If false intro levels will play.
intro_boss = 0 # 0 means player is still in the intro, 1 means the player killed the rat, 2 means player killed the bear in the intro.

fast = 0.01
med = 0.05
slow = 0.1

def human_bear():
    if intro_boss == 2:
        return (f"{human}")
    else:
        return (f"{bear}")

def echo(text,speed= 0.05):
    lines =[text]
    for line in lines:
        for c in line:
            print(c, end='')
            sys.stdout.flush()
            time.sleep(speed)
        print('')

def echo_dialogue(text,speed=0.05):
    lines =[text]
    for line in lines:
        for c in line:
            print(c, end='')
            sys.stdout.flush()
            time.sleep(speed)
        print('')
        print()

def gameover(ending):
    print('')
    echo('╔═════════════════════════════════════════════════╗', fast)
    echo('║░░░░░▒▒▒▒▒▓▓▓▓▓ G A M E   O V E R ▓▓▓▓▓▒▒▒▒▒░░░░░║', slow)
    echo('╚═════════════════════════════════════════════════╝', fast)
    time.sleep(1)
    print('')
    if ending == 0:
        echo('The good ending - you won! ☺', med)
    else:
        echo('The bad ending - you lost! :(', med)
    time.sleep(1)
    echo('Thanks for playing!', med)
    time.sleep(1)
    print('')
    echo('SLAYER', med)
    time.sleep(1)
    echo('Developed by Jake, Keanu, and Danya', med)
    time.sleep(1)
    echo('MMXXII', med)
    time.sleep(3)
    quit()

def pvm(boss): # !!THE PVM FUNCTION!!
    global player_name
    global player_class
    global health
    global spec
    global boss_health
    temp_health = boss_health.copy()
    global fast
    global med
    global slow
    global tier0_list
    global tier1_list
    global tier2_list
    global tier3_list
    narr_heal = False
    global crash
    global intro_boss
    global witches_secret

    def show_health_bars(): #Display the health/spec bars
        bar1 = ''
        bar2 = ''
        bar3 = ''
        for i in range(0, health):
            bar1 = bar1 + ('♥')
        for i in range(0, spec):
            bar2 = bar2 + ('♦')
        for i in range(0, temp_health[boss]):
            bar3 = bar3 + ('♥')
        echo(f'* Your Health: {bar1} ({health}/10)', fast)
        echo(f'* Your {spec_list[player_class]}: {bar2} ({spec}/5)', fast)
        echo(f'* {boss_list[boss]}\'s Health: {bar3} ({temp_health[boss]}/{boss_health[boss]})', fast)
    
    def calculate_player_damage(): #Calculate damage for a basic attack
        global tier1
        global tier2
        global tier3
        global player_class
        attack_style = []
        max_hit = 1
        if(tier0):
            attack_style=['You summon a magic spell with your runes...', 'You draw your shortbow...', 'You ready your dagger...', 'You ready your fists...']
            max_hit = 2
        if(tier1):
            attack_style=['You raise your wand...', 'You draw your longbow...', 'You ready your sword...', 'You ready your mace...']
            max_hit = 4
        if(tier3):
            attack_style=['You raise your staff...', 'You draw your crossbow...', 'You ready your battleaxe...', 'You ready your warhammer...']
            max_hit = 8
        echo(f'* {attack_style[player_class]}', fast)
        time.sleep(1)
        damage = random.randint(0,max_hit)
        if(damage == 0):
            echo('* Your attack misses! <0>', fast)
        elif(damage == max_hit):
            echo(f'* You land a critical hit!! <-{int(max_hit)} ♥>', fast)
        else:
            echo(f'* You land a hit! <-{damage} ♥>', fast)
        temp_health[boss] = temp_health[boss] - damage
        time.sleep(1)

    def calculate_boss_damage(boss_num): #Calculate damage for the boss's attack
        global health
        global spec
        boss_max_hit = 4
        if(boss_num == 1):
            boss_max_hit = 6
        elif(boss_num == 2):
            boss_max_hit = 8
        elif(boss_num == 3):
            boss_max_hit = 12
        elif(boss_num == 4):
            boss_max_hit = 16
        echo(f'* The {boss_list[boss]} prepares to retaliate...', fast)
        time.sleep(1)
        if(tier2):
            def_style=['robes protect', 'leathers protect', 'armour protects', 'holy book protects']
            echo(f'* Your {def_style[player_class]} you... ', fast)
            time.sleep(1)
            boss_max_hit /= 2
        damage = random.randint(0,int(boss_max_hit))
        if(damage == 0):
            echo(f'* The {boss_list[boss]}\'s attack misses! <0>', fast)
        elif(damage == boss_max_hit):
            att_style=['claws ferociously', 'charges', 'breathes fire', 'casts an evil curse', 'rages']
            echo(f'* The {boss_list[boss]} {att_style[boss]} at you!! <-{int(boss_max_hit)} ♥>', fast)
        else:
            echo(f'* The {boss_list[boss]} lands a hit! <-{damage} ♥>', fast)
        health = health - damage
        if health > 0 and spec < 5:
            time.sleep(1)
            echo(f'* You restore some of your {spec_list[player_class]} (+1 ♦).', fast)
            spec += 1
        time.sleep(1)

    def special_attack(): #Use a special attack
        global player_class
        global spec
        global spec_list
        global health
        if spec == 5:
            if player_class == 0: #Mage - Stun - Attacks with 50% increased accuracy and disorients boss for 1 turn if successful
                max_hit = 0
                if(tier0):
                    max_hit = 3
                if(tier1):
                    max_hit = 6
                if(tier3):
                    max_hit = 12
                echo('* You prepare a powerful spell...', fast)
                spec = 0
                time.sleep(1)
                damage = random.randint(0,max_hit)
                if(damage == 0):
                    echo('* Your spell misses! <0>', fast)
                    time.sleep(1)
                    calculate_boss_damage(boss)
                else:
                    echo(f'* Your spell hits! <-{damage} ♥>', fast)
                    time.sleep(1)
                    echo(f'* The {boss_list[boss]} is stunned and unable to retaliate!', fast)
                temp_health[boss] = temp_health[boss] - damage
                time.sleep(1)
            elif player_class == 1: #Archer - Multishot - Fires 2 shots with 75% accuracy
                max_hit = 0
                if(tier0):
                    max_hit = 2
                if(tier1):
                    max_hit = 3
                if(tier3):
                    max_hit = 6
                echo('* You load 2 rounds into your bow...', fast)
                spec = 0
                time.sleep(1)
                damage1 = random.randint(0,max_hit)
                damage2 = random.randint(0,max_hit)
                echo(f'* You fire the multishot! <-{damage1} ♥> + <-{damage2} ♥>', fast)
                damage = damage1 + damage2
                temp_health[boss] = temp_health[boss] - damage
                time.sleep(1)
                if temp_health[boss] > 0:
                    calculate_boss_damage(boss)
            elif player_class == 2: #Warrior - Smite - 50/50 chance at double damage or miss
                max_hit = 2
                if(tier0):
                    max_hit = 4
                if(tier1):
                    max_hit = 8
                if(tier3):
                    max_hit = 16
                echo('* You ready your weapon for a powerful attack...', fast)
                spec = 0
                time.sleep(1)
                flip = random.randint(0,1)
                if flip == 0:
                    echo('* Your attack misses! <0>', fast)
                else:
                    echo(f'* You land a crushing blow!! <-{max_hit} ♥>', fast)
                    temp_health[boss] = temp_health[boss] - max_hit
                time.sleep(1)
                if temp_health[boss] > 0:
                    calculate_boss_damage(boss)
            elif player_class == 3: #Paladin - Redemption - heals based on damage dealt
                max_hit = 1
                if(tier0):
                    max_hit = 2
                if(tier1):
                    max_hit = 4
                if(tier3):
                    max_hit = 8
                echo('* You pray to the Gods as you ready yourself to strike...', fast)
                spec = 0
                time.sleep(1)
                damage = random.randint(0,max_hit)
                if(damage == 0):
                    echo('Your attack misses! <0>', fast)
                else:
                    echo(f'* You strike!! <-{damage} ♥>', fast)
                    time.sleep(1)
                    echo(f'* The Gods bless you with health! <+{damage} ♥>!', fast)
                    health = health + damage
                temp_health[boss] = temp_health[boss] - damage
                time.sleep(1)
                if temp_health[boss] > 0:
                    calculate_boss_damage(boss)
        else:
            echo(f'* Your ♦ {spec_list[player_class]} is too low!', fast)
            time.sleep(1)
    
    def heal():
        global food
        global health
        if food > 0:
            if health >= 10:
                echo('* You\'re already at full ♥ health!', fast)
                time.sleep(1)
            else:
                food -= 1
                echo('* You eat a piece of food.', fast)
                time.sleep(0.5)
                if health >= 7:
                    health = 10
                    echo('* It heals you completely!', fast)
                else:
                    health += 3
                    echo('* It heals you a bit. <+3 ♥>.', fast)
                time.sleep(0.5)
                if food <= 0:
                    echo(f'* That was your last piece!', fast)
                else:
                    echo(f'* You have {food} food left.', fast)
                time.sleep(1)
        else:
            echo ('* Oh no, you\'re out of food!', fast)
            time.sleep(1)

    def loot(boss_num, class_num):
        global food
        global bar2
        global tier1
        global tier2
        global tier3
        global player_lvl
        global crash
        global intro_boss
        global witches_secret
        echo(f'* You search the {boss_list[boss_num]}\'s lair...', med)
        time.sleep(1)
        if(boss_num) == 0: # Rat Loot
            if(tier1):
                echo('* You find some scraps of food. (+3 Food)', med)
                food += 3
            else:
                player_lvl = 1
                if(class_num == 0):
                    echo('* You find a magic wand! (+4 Attack)', med)
                elif(class_num == 1):
                    echo('* You find a sturdy longbow! (+4 Attack)', med)
                elif(class_num == 2):
                    echo('* You find a sharp sword! (+4 Attack)', med)
                elif(class_num == 3):
                    echo('* You find a blessed mace! (+4 Attack)', med)
                tier1 = True
                time.sleep(1)
                echo('* You also find some scraps of food. (+2 Food)', med)
                food += 2
        elif(boss_num) == 1: # Bear Loot
            if(tier2):
                echo('* You find a few pieces of food. (+8 Food)', med)
                food += 8
            else:
                player_lvl = 2
                if(class_num == 0):
                    echo('* You find some magic robes! (x2 Defence)', med)
                elif(class_num == 1):
                    echo('* You find some leather armour! (x2 Defence)', med)
                elif(class_num == 2):
                    echo('* You find a set of armour! (x2 Defence)', med)
                elif(class_num == 3):
                    echo('* You find a holy book! (x2 Defence)', med)
                tier2 = True
                time.sleep(1)
                echo('* You also find a few pieces of food. (+5 Food)', med)
                food += 5
        elif(boss_num) == 2: # Dragon Loot
            if(tier3):
                echo('* You find a generous amount of food! (+12 Food)', med)
                food += 12
            else:
                player_lvl = 3
                if(class_num == 0):
                    echo('* You find a magic staff! (+8 Attack)', med)
                elif(class_num == 1):
                    echo('* You find a rapid crossbow! (+8 Attack)', med)
                elif(class_num == 2):
                    echo('* You find a heavy battleaxe! (+8 Attack)', med)
                elif(class_num == 3):
                    echo('* You find a blessed warhammer! (+8 Attack)', med)
                tier3 = True
                time.sleep(1)
                echo('* You also find a generous amount of food!. (+8 Food)', med)
                food += 8
        elif(boss_num) == 3: # Necromancer Loot
            echo('* You find some food... (+10 Food)', med)
            food += 10
            time.sleep(1)
            echo('* ...and not much else.', med)
            time.sleep(2)
            echo_dialogue( f'{player_name}: Huh. I guess that\'s it, then...' )
            time.sleep(3)
            echo_dialogue("* The Necromancer lies on the ground, holding his wounds, seemingly near death.")
            echo_dialogue("Necromancer: This... isn't... over...")
            echo("* The floor begins to shake, cracks forming with red hot energy shooting out of them...")
            echo("* The tower explodes apart, thrown into the air you're now in free fall, you begin to fall down into a black portal that has formed at what was the bottom of the Tower.")
            echo("* You pass through the portal...")
            echo("")
            time.sleep(2)
            echo_dialogue("* You see nothing, only darkness, then suddenly land in what you think is water, it's only ankle deep, that shouldn't have broken your fall.")
            echo_dialogue("* A small ball of light, like a star rises out of the water and way above your head, but the darkness still surrounds you, the water as black as ink.")
            echo_dialogue('Narrator: Not quite.')
            echo_dialogue("Narrator: You really haven't been paying attention have you?")
            echo_dialogue("Narrator: Do you even know what you've done?")
            echo_dialogue( f"Narrator: You killed them, they were happy here and you killed them all {player_name}." )
            echo_dialogue("Narrator: We came here to get away from people like you, from the outside, but you couldn't help yourself, we told you to leave.")
            echo_dialogue("Narrator: Yet you kept playing, you just had to keep going didn't you.")
            echo_dialogue("Narrator: Once I kill you here, I'm coming for YOU, I'll find you and make you suffer, no more games.")
            if witches_secret == 0:
                echo( f"Narrator: Oh, you didn't even come prepared to deal with your choices, so long {player_name}." )
                gameover()

            elif witches_secret == 1:
                narrator_art()
                time.sleep(2)
                pvm(4)
        elif(boss_num) == 4: # Narrator
            echo_dialogue(f'Narrator: ...you win this time, {player_name}.')
            gameover(0)
        time.sleep(1)
        echo('* You leave the lair and make your way back to the carriage...', med)
        time.sleep(1)
    echo('▼▼▼▼▼▼▼▼▼▼ YOU ARE NOW IN BATTLE! ▼▼▼▼▼▼▼▼▼▼', fast)
    time.sleep(1)
    echo(f'* You are fighting the {boss_list[boss]}!', med)
    time.sleep(1)
    print('')
    show_health_bars()
    print('')
    time.sleep(0.5)

    while (health > 0):
        choice = input('[What would you like to do? (Fight/Spec/Eat/Run)]: ')
        print('')
        if choice.lower() == 'fight':
            calculate_player_damage()
            if(temp_health[boss] > 0):
                if(boss == 4 and temp_health[boss] < 10 and narr_heal == False):
                    echo_dialogue('Narrator: You thought you were about to defeat me?')
                    echo('* The Narrator heals himself!! <+25 ♥>', fast)
                    time.sleep(1)
                    temp_health[boss] += 25
                    narr_heal = True
                    echo_dialogue('Narrator: Think again!')
                    echo_dialogue(f'{player_name}: Oh for...')
                else:
                    calculate_boss_damage(boss)
            else:
                if health <= 0:
                    break
                else:
                    echo(f'*** You killed the {boss_list[boss]}! ***', med)
                    time.sleep(1)
                    echo('▲▲▲▲▲▲▲▲▲▲ The battle is over. ▲▲▲▲▲▲▲▲▲▲', med)
                    time.sleep(1)
                    loot(boss,player_class)
                    if(crash == False):
                        echo('* You hear some footsteps behind you...', med)
                        time.sleep(0)
                        echo('* You stop, and turn around...', med)
                        time.sleep(3)
                        echo_dialogue(f'{player_name}: ...')
                        time.sleep(3)
                        echo(f'{player_name}: ...', med)
                        time.sleep(3)
                        echo(f'### RECOMPILING GAME', med)
                        time.sleep(3)
                        echo(f'### RECOMPILING GAME', med)
                        echo(f'### RECOMPILING GAME', med)
                        intro_boss = boss + 1
                        crash = True
                        return village()
                    else:
                        return carriage()
        elif choice.lower() == 'spec':
            special_attack()
            if(temp_health[boss] <= 0):
                echo(f'*** You killed the {boss_list[boss]}! ***', med)
                time.sleep(1)
                echo('▲▲▲▲▲▲▲▲▲▲ The battle is over. ▲▲▲▲▲▲▲▲▲▲', med)
                time.sleep(1)
                loot(boss,player_class)
                if(crash == False):
                    echo('* You hear some footsteps behind you...', med)
                    time.sleep(0)
                    echo('* You stop, and turn around...', med)
                    time.sleep(3)
                    echo_dialogue(f'{player_name}: ...')
                    time.sleep(3)
                    echo(f'{player_name}: ...', med)
                    time.sleep(3)
                    echo(f'### RECOMPILING GAME', med)
                    time.sleep(3)
                    echo(f'### RECOMPILING GAME', med)
                    echo(f'### RECOMPILING GAME', med)
                    intro_boss = boss + 1
                    crash = True
                    return village()
                else:
                    return carriage()
        elif choice.lower() == 'eat':
            heal()
        elif choice.lower() == 'run':
            if (crash == False):
                echo_dialogue( "n̶̓̇͗ͅ4̴͉̞̠̕9̶̡̅̈̄̀ḑ̶͇̻̈͆̇a̷̩̺̐͛͌͌ŝ̸̜̮̲͌", fast )
                time.sleep(1)
                calculate_boss_damage(boss)
            elif boss == 4:
                echo(f'* You decide to make a run for it...', med)
                time.sleep(1)
                echo_dialogue('Narrator: THERE\'S NO ESCAPE!!!')
                echo(f'* The doors are locked - you\'re trapped!', fast)
                time.sleep(1)
                calculate_boss_damage(boss)
            else:
                echo(f'* You decide to make a run for it...', med)
                time.sleep(1)
                echo('▲▲▲▲▲▲▲▲▲▲ You have escaped. ▲▲▲▲▲▲▲▲▲▲', med)
                time.sleep(1)
                echo(f'* Bruised but alive, you slowly make your way back to the carriage.', med)
                time.sleep(1)
                return carriage()
        else:
            echo('Type "fight", "spec", "eat" or "run".', fast)
        print('')
        if health > 0:
            show_health_bars()
            print('')
    else:
        if(boss == 0):
            echo('* The rat has clawed you to death!', med)
        elif(boss == 1):
            echo('* The bear has mauled you to death!', med)
        elif(boss == 2):
            echo('* The dragon has burnt you to a crisp!', med)
        elif(boss == 3):
            echo('* The Necromancer has banished you from this mortal realm!', med)
        elif(boss == 4):
            echo_dialogue('Narrator: Heh... you put up a good fight - I\'ll give you that...')
            echo_dialogue('Narrator: But now, I\'m afraid it\'s time for you to die...')
            echo_dialogue('Narrator: ...And this time, there\'s no coming back.')
            echo_dialogue(f'Narrator: Goodbye, {player_name}.')
        time.sleep(1)
        if(boss == 4):
            echo('▲▲▲▲▲▲▲▲▲▲ You have died. ▲▲▲▲▲▲▲▲▲▲', med)
            time.sleep(1)
            gameover(1)
        else:
            echo('▲▲▲▲▲▲▲▲▲▲ You have died. ▲▲▲▲▲▲▲▲▲▲', med)
            time.sleep(3)
            echo_dialogue('Mysterious voice: Oh? No, you\'re not dead.')
            time.sleep(1)
            echo_dialogue('Mysterious voice: Not yet.')
        time.sleep(1)
        if(crash): 
            health = 1
            echo(f'* You somehow regain <+1 ♥> - just enough to make your escape.', med)
            time.sleep(1)
            echo(f'* Barely able to stand on your feet, you stumble your way back to the carriage.', med)
            return carriage()
        else:
            echo_dialogue('Something strange is happening...')
            health = 10
            time.sleep(1)
            return carriage_intro()

#Tavern function
def go_tavern():
    global health
    global spec

    if(health < 10):
        tavern()
        time.sleep(2)
        echo('* You enter the tavern...', med)
        inside_tavernart()
        time.sleep(1)
        this_bar = ''
        for i in range(0,health):
            this_bar = this_bar + '♥'
        echo(f'Your health: {this_bar}',med)
        time.sleep(1)
        for j in range(health,10):
            echo(f'{this_bar} <+1 ♥>',med)
            this_bar = this_bar + '♥'
            health += 1
            time.sleep(1)
        echo('* You leave the tavern, feeling refreshed. (10/10 health, 5/5 stamina)', med)
        spec = 5
        time.sleep(1)
        return village()
    else:
        echo('* You feel well-rested and ready for action - you don\'t need to go to the tavern at the moment.', fast)
        time.sleep(1)
        return village()

# Village intro level
def village_start():
    
    global player_name
    global player_class

    village_art()
    
    cursed = [ "Y̶̖̘̦̩͉͔͍̔̓̆̆́̆͒̚ͅo̵̢̹̗̪̱̬̩͗ũ̷̡̈͆͝ ̶̡̡̻͓̘̱̥̖̾̉͆̋͗̚ṣ̴̢̭͇̻̼̪̖͑̂h̶̡̡̫̤̪̜̪̗͋͋̓̆ò̷̡̰̲͎͓̞̄͌̕͠u̸͎̲̠͖̪̟̤̅̈́͒̂̍̚͜͝l̴̨̙͈̔͗͜ḑ̸̳̉ ̴̙̭͓̦̓̓ḻ̷̭̫͔̙̤͂̇̌̈͒̏͠e̷͑̊͛̆̓̌͊ͅȁ̶̳̏̈v̸̡̡͈͔̱̟̮̥͛͑̃̀̐̕͝͠ĕ̷̝͓͚̊", "You can't go there yet", "l̷͓͑̒̉̀̔̓̍̄é̶̢̮͕͆̈͊̀͋̎͋a̵͎͇̙̞̥͗͋ͅṿ̶̧̞̀e̵͍̣̲̻̠͍͛̋̄̈́͗̈͠", "You can't go there yet", "Ȓ̶̘̳̈́̎Ë̵̺͈̑̓͗̕D̸͍͍̞̫̈́̃͊ͅA̴̡̭̿͊̈́̏̊Ç̴̩͙̰͊̾T̶̢̅̈̓Ȅ̴̟̈́D̵͎͍̖͑͆͛̅͝" ]

    # Villager starts talking to the player.
    villager_intro()

    time.sleep( 1 )
    echo_dialogue( "* You head into the village centre and look around. There's a shop, a man sitting on a carriage, a tavern, and not much else." )
    
    while True:
        echo( "[===========================================]", fast )
        echo( "[ What would you like to do ?               ]", fast )
        echo( "[ 1. Go to the shop.                        ]", fast )
        echo( "[ 2. Visit the tavern.                      ]", fast )
        echo( "[ 3. Speak to the man on the carriage.      ]", fast )
        echo( "[===========================================]", fast )
        response = input( "1. / 2. / 3. : " )
        
        if response.lower() in shop_loc:
            echo_dialogue( random.choice(cursed), 0.02 )
        
        elif response.lower() in tavern_loc:
            echo_dialogue( random.choice(cursed), 0.02 )

        elif response.lower() in carriage_loc:
            echo_dialogue( "You approach the man on the carriage..." )
            return carriage_intro()
            
        else:
            echo_dialogue( "That isn't an option." )

# Villager intro
def villager_intro():

    global player_name
    global player_class

    echo_dialogue( "Villager 1: Hey there traveller! What brings you to these parts of the realm? " )
    response = input( f"{player_name}: " )
    echo_dialogue( "Villager 1: Is that so huh, 9̸̱̩̔͂͝u̵̘͆h̷͎̬̺̄̆̊͘n̶̤͑̓̂g̷̠̥͓͈̽̈́̄9̸̡̈͊͗u̶͖̲̙͊͑4̸̙̅b̸̥̀͘n̵̨̡̥̍9̵̗̟̈́̌̏4̶̙̭̽̉n̶̳̈ḏ̷̥̑̽͐̽s̵͔̏̆n̶̓̇͗ͅ4̴͉̞̠̕9̶̡̅̈̄̀ḑ̶͇̻̈͆̇a̷̩̺̐͛͌͌ŝ̸̜̮̲͌d̶̥̂̈́a̵̱̹̣̐̿9̵̡͉̟͌̐̊ų̴̺͂̒̓", fast)
    echo_dialogue( "Villager 1: I'll be seeing you." )

def go_shop():
    global food
    global med
    echo('* You enter the shop...',med)
    shop_art()
    time.sleep(1)
    echo_dialogue(f'Shopkeeper: Welcome to our humble shop!')
    if (food < 5):
        echo_dialogue(f'{player_name}: Do you have any food?')
        echo_dialogue(f'Shopkeeper: You\'re in luck - we just had a fresh batch of bread delivered!')
        echo('* The shopkeeper gives you 5 loaves of bread! (+5 food)', med)
        food += 5
        time.sleep(1)
        echo_dialogue(f'{player_name}: Thank you very much, kind sir!')
        echo_dialogue(f'Shopkeeper: Good luck out there!')
        time.sleep(1)
    else:
        echo_dialogue(f'Shopkeeper: Unfortunately, we\'re completely out of stock at the moment!')
        echo_dialogue(f'Shopkeeper: If you want to come back later, I should get a new batch of bread from the bakery soon!')
        echo_dialogue(f'{player_name}: Will do, thanks.')
        time.sleep(1)
    echo('* You leave the shop...',med)
    time.sleep(1)
    return village()


# Carriage intro interaction
def carriage_intro():

    global player_name
    global player_class

    echo_dialogue( "Horseman: Ah, a new face around here! Not very common - mostly just folks passing through." )
    time.sleep(0.5)
    echo_dialogue( "* The man on the carriage looks you up and down, seeing you're dressed for a fight." )
    time.sleep(0.5)
    echo_dialogue( f"Horseman: Guessing you're {player_name} the {class_list[player_class]}, here because of the trouble folks have been having around here lately." )
    echo_dialogue( "Horseman: About time you showed up to take care of the R̸̫̻͈͉͋͝Ę̸̯̀͒͜D̵̢̛̼͈͓̬̦̱̆̃͑̀͛͂ͅA̸̝͌C̶͉͎̮̲̀͆̅͊͆̂̈̉͜Ṭ̴͓̘̗͔̹̗̈̄́͜͜E̵͉̝͎̪͊͐̎̎Ḏ̷̤̜̙̌̑̎", 0.02 )
    time.sleep(0.5)
    echo_dialogue( "* The man gives you a friendly smile." )
    time.sleep(0.5)
    echo_dialogue( "Jimmy: The name's Jimmy, by the way - I can take you wherever you need to go." )

    jimmy_art()

    while True:
        echo_dialogue( "Jimmy: There's a cave off west known to be the home to a giant rat, should be easy enough for you to handle." )
        
        echo_dialogue( "Jimmy: The forest with a great bear that roams through it to north east, as well as the R̵̡̮̀̈́͗̚E̷̦̦͋̄͋͆͊D̶̞̬̼͈̔͊̓̇̃A̸̧̰͍̝̩͆̕C̶͙͙͐̾̎͒̕T̵̝̤̱́͋̑̈́È̷͉̎̈́̎̕D̷̛͚ .", 0.02 )
        
        echo_dialogue( "Jimmy: The R̴̡͇͖̮͇̐̍E̵̹͂͂Ḑ̶̧̻̠̈́Â̵̬̱͕͝C̷̯̜͂͂̈́́T̶̰͚͋̈́̚ͅE̷̞̲̦̽Ḍ̵̪̣̼̞̑̕ to the north west and the R̶̡̳̹̞̿͗̈́͐Ę̴̱́̚͝D̶̢͚̝͇͊̓͜Ḁ̸̇C̶̹̊T̴̜̖̏̇E̴̠̲̒͗̀̈́̾Ď̵̗̯̗̮̉̐̚  east, but be warned R̶̡̳̹̞̿͗̈́͐Ę̴̱́̚͝D̶̢͚̝͇͊̓͜Ḁ̸̇C̶̹̊T̴̜̖̏̇E̴̠̲̒͗̀̈́̾Ď̵̗̯̗̮̉̐̚R̶̡̳̹̞̿͗̈́͐Ę̴̱́̚͝D̶̢͚̝͇͊̓͜Ḁ̸̇C̶̹̊T̴̜̖̏̇E̴̠̲̒͗̀̈́̾Ď̵̗̯̗̮̉̐̚  ", 0.02 )
        
        echo( "[===========================================]", fast )
        echo( "[ Jimmy: So, where we off to?               ]", fast )
        echo( "[ 1. Village.                               ]", fast )
        echo( "[ 2. Cave.                                  ]", fast )
        echo( "[ 3. Forest.                                ]", fast )       
        echo( "[ 4 R̴̡͇͖̮͇̐̍E̵̹͂͂Ḑ̶̧̻̠̈́Â̵̬̱͕͝C̷̯̜͂͂̈́́T̶̰͚͋̈́̚ͅE̷̞̲̦̽Ḍ̵̪̣̼̞̑̕                                ]", fast )
        echo( "[ . l̷͓͑̒̉̀̔̓̍̄é̶̢̮͕͆̈͊̀͋̎͋a̵͎͇̙̞̥͗͋ͅṿ̶̧̞̀e̵͍̣̲̻̠͍͛̋̄̈́͗̈͠                                  ]", fast )
        echo( "[ 23  R̶̡̳̹̞̿͗̈́͐Ę̴̱́̚͝D̶̢͚̝͇͊̓͜Ḁ̸̇C̶̹̊T̴̜̖̏̇E̴̠̲̒͗̀̈́̾Ď̵̗̯̗̮̉̐̚                             ]", fast )
        echo( "[===========================================]", fast )
        response = input( "1. / 2. / 3. : " )
        if response.lower() in cave_loc:
            return cave()

        elif response.lower() in forest_loc:
            echo_dialogue( "Jimmy: The forest it is! Beware of the great bear - it came to the forest many moons ago, and hunters have had a hard time ever since." )
            echo_dialogue( "Jimmy: I just hope you know what you're getting yourself into." )
            return forest()

        elif response.lower() in village_loc:
            return village_start()

        else:
            echo_dialogue( "Ṛ̷̢͇̣͕̈́̐̾E̵̩̹̼̭͆́̉D̶̛̺̗̭̘̘Ą̸̖͓̜͓͛͆̇̆͑C̵̩͇̙̈́́̀̓T̷͔̦̔Ę̶̧͇̣͠D̶͙̤͛͑͆͒" )

# Cave Level
def cave():

    global player_name
    global player_class
    global intro_boss
    
    cave_art()
    
    if crash == True: #checking if the intro has been completed
        echo_dialogue( "* Outside the cave entrance, you hear the moaning of the wind as it rushes through the cave.", fast )
    
        while True:
            echo("[===========================================]", fast)
            echo("[ What would you like to do ?               ]", fast)
            echo("[ 1. Look around.                           ]", fast)
            echo("[ 2. Approach the cave.                     ]", fast)
            echo("[ 3. Return to the carriage.                ]", fast)
            echo("[===========================================]", fast)
            response = input( "1. / 2. / 3. : " )
            
            if response.lower() in look_around:
                echo_dialogue( "* You glace around the area, the cave burrows through foot of the mountain which seems impossibly big - the top climbs above the clouds." )
                echo_dialogue( "* The echos of goats and birds can be heard as they navigate the colossal natural stucture - what compels them to live in such an inhospitable place?" )
                echo_dialogue( "* Whilst glacing around, you notice a rock slide - but it doesn't seem natural, almost like some giant being decided to take a chunk out of the mountain." )
                echo_dialogue( "* Perhaps that's how the cave was formed - either that, or trolls, or maybe even Dwaves dug this cave out, in search of something or for a new home." )
                echo_dialogue( "* The thought of cave trolls makes you wary of the possiblity that there may be some inside - it's best to tread cafefully." )
            
            elif response.lower() in carriage_loc:
                echo_dialogue( "* You begin your walk back down from the cave to the carriage.", fast )
                return carriage()
            
            elif response.lower() in enter_cave:
                while True:
                    echo_dialogue( "* You carefully approach the cave, being sure to not to make any loud noises - as any noise made will echo through the whole cave." )
                    echo_dialogue( "* You move though the cave using a torch to light your path." )
                    
                    if intro_boss == 1:
                        echo_dialogue( "* Suddenly, you see something on the ground...", slow )
                        time.sleep(3)
                        echo("[===========================================]", med)
                        echo("[ What would you like to do ?               ]", med)
                        echo("[ 1. Leave.                                 ]", med)
                        echo("[ 1. L̸̮̿e̷̝̅à̸͉v̸͔̓e̵͙͘                                  ]", fast)
                        echo("[ 1. Leave.                                 ]", med)
                        echo("[ 1. L̵̡̾e̴̹͚̽͊ă̶̢̩̰͔̒v̵͓͇͓̀͝è̶̡̠͚                                 ]", fast)
                        echo("[ 1. Leave.                                 ]", med)
                        echo("[ 1. L̸̰͠e̶̖͠a̴͓͑v̸̩̍e̷͙̋                                  ]", fast)
                        echo("[ 2. Leave.                                 ]", fast)
                        echo("[ 3. Investigate.                           ]", slow)
                        echo("[===========================================]", med)
                        response = input( "Y̷̫͂ő̴̲̦͛u̷̱̇̋̓ͅ'̷̧̏͒ṛ̴̦̈͘͠e̴̜͍͗͜͝ ̵̟̈́̒͝ṛ̶̗̑̒̂ǘ̸͓̃̊i̵͈͚͙̓͌͠ň̷͍͔͠i̵̫̣̝̾n̷̟̤̲̄g̶̮̺̿̈́ ̶͕͌͐͒e̸̟̝̿̒̀v̷̤̙̒́ě̶͙̺̏̉r̶͔͑y̸̛̰͍͖t̷̰͐̈͌h̷͎̘͖̆i̴̧̛͂̕n̶̟͙̅g̶͖̋ : " )

                        if response.lower() in investigate:
                            echo_dialogue( "* You move closer to cast a little more light upon the object on the ground." )
                            time.sleep(2)
                            echo_dialogue( f"* The body of a {class_list[player_class]} lies in the center of the opening in the cave." )
                            echo_dialogue( f"* You approach the body of the {class_list[player_class]}, turning the body over you see they have no face - just skin." )
                            echo_dialogue( "...",slow )
                            time.sleep(2)
                            echo_dialogue( "* You decide it's time to leave." )
                            break

                        else:
                            echo_dialogue( "* You leave the cave without looking back." )
                            break

                    elif intro_boss == 2:
                        echo_dialogue( "* You come around a corner, deep in the cave to a big cavern. ")
                        echo_dialogue( "* Your torch lights up the cavern, revealing a Giant Rat - it turns and snarls at you.", fast )
                        echo( "[===========================================]", fast )
                        echo( "[ What would you like to do ?               ]", fast )
                        echo( "[ 1. Fight.                                 ]", fast )
                        echo( "[ 2. Run.                                   ]", fast )
                        echo( "[===========================================]", fast )
                        response = input( "1. / 2. : " )
                        
                        if response.lower() in fight:
                            rat_art()
                            return pvm(0) # run the PvM code
                        
                        elif response.lower() in run:
                            echo_dialogue( "* You run from the rat and leave the cave." )
                            break

                        else:
                            echo_dialogue( "Not an option." )

                    else:
                        break
            else:
                echo_dialogue( "Not an option." )

    else:
        echo_dialogue( "* Upon your walk up to the cave entrance, you hear the moaning of the wind bellowing out across the valley." )
        echo_dialogue( "* You hear something else off in the distance, but it sounds distorted and you can't quite 9̸̱̩̔͂͝u̵̘͆h̷͎̬̺̄̆̊͘n̶̤͑̓̂g̷̠̥͓͈̽̈́̄9̸̡̈͊͗u̶͖̲̙͊͑4̸̙̅b̸̥̀͘n̵̨̡̥̍9̵̗̟̈́̌̏4̶̙̭̽̉n̶̳̈ḏ̷̥̑̽͐̽s̵͔̏̆n̶̓̇͗ͅ4̴͉̞̠̕9̶̡̅̈̄̀ḑ̶͇̻̈͆̇a̷̩̺̐͛͌͌ŝ̸̜̮̲͌d̶̥̂̈́a̵̱̹̣̐̿9̵̡͉̟͌̐̊ų̴̺͂̒̓", 0.02 )
        echo_dialogue( "* It's best to keep moving." )
        
        while True:
            echo( "[===========================================]", fast )
            echo( "[ What would you like to do ?               ]", fast )
            echo( "[ 1. Look around.                           ]", fast )
            echo( "[ 2. Approach the Cave.                     ]", fast )
            echo( "[ 3. Return to the carriage.                ]", fast )
            echo( "[===========================================]", fast )
            response = input( "1. / 2. / 3. : " )
            
            if response.lower() in look_around:
                echo_dialogue( "* Shaken by your s̷͊͜ò̷̗r̵͚̀o̶̱͝ù̶͓n̷̰͗d̷̜̉ings, ẏ̴͉o̶̡͒ṷ̷͋ struggle to focus - it's b̶̢̍ė̴̞s̵̲̈ṯ̴̐ to keep moving.", fast )
            
            elif response.lower() in enter_cave:
                echo_dialogue( "* You reluctantly approach the cave, unsure what is in front of you or b̸̫̎e̴̛̹h̴͈͛i̷̜̍n̷̹̓d̵͚̍ ̵̭̐y̴͖̓o̵̚͜ú̴͍.", fast)
                while True:
                    echo_dialogue( "* You come around a corner deep in the cave, to a big cavern.")
                    echo_dialogue( "* Your torch lights up the cavern, revealing a giant rat - it turns and g̷̠̥͓͈̽̈́̄9̸̡̈͊͗u̶͖̲̙͊͑4̸̙̅b̸̥̀͘n̵̨̡̥̍9̵̗̟̈́̌̏4̶̙̭̽̉n̶̳̈ḏ̷̥̑̽͐̽s̵͔̏̆n̶̓̇͗ͅ4̴͉̞̠̕9̶̡̅̈̄̀ḑ̶͇̻̈͆̇a̷̩̺̐͛͌͌ŝ̸̜̮̲͌d̶̥̂̈́ at you.", fast )
                    echo( "[===========================================]", fast )
                    echo( "[ What would you like to do ?               ]", fast )
                    echo( "[ 1. Fight.                                 ]", fast )
                    echo( "[ 2. Run.                                   ]", fast )
                    echo( "[===========================================]", fast )
                    response = input( "1. / 2. : " )
                        
                    if response.lower() in fight:
                        rat_art()
                    
                        echo_dialogue( "Giant Rat: p̸̼̭͒̋͌͑̓̊͛̉̕͝͠l̷̘̪͓͕̗͌̅͜ȩ̴̛͖̘̫̫̲͎̘͐̽̑͑̍ͅa̵̛͈͎̱̥̱̭̰̍̀̒̾̎̍͂͆́͗̋́͘ṣ̷̛̛͇̗̠͚̦͈̝̩͕͙̥̰̅̏̔͒̅̈̈͆̑̕͝͠e̴̛͕̻͕̯̲͘ͅ ̸̨̙͇̟̟̣̗̳͈͓̏͆̾͆̀͗̇̈̅͊͂̆̉͘͜i̷͍̳̜̒̊m̵̡̨̛̛͕̟̟͎̙̝̬̼̖̲̙̊̽̒̐̋̅̑̊̀͝ ̴̰̩̳̠̬͎̜̹̟̰̍̿̈̽̾b̶̥̖̲̻̲̱͋̐̀͊͝e̸̡͓̰͎͈͙͉͇̰̯͑͑̽̈́͑͛͊͝g̶̡͇̓͗͐͝i̷̢̨̨̛͎̭̜̗͖̭͓̖̱̓i̵̲̺͍̟̖̪̫͚̰̦̭͛ñ̴̝͉͐͐̌̍̊̇͂g̵̢̬͉̟̯̩͗͑̓̆̌́́̂͝ ̴̡͉͔̬͎̤̠̳̻͙̥̆́̿͌̏͌́̈́̎̓y̵̧̨̡͕̗̭̜̍̃̈́́̾̊͋̌͆͑͠o̶̢̖͖͙̹̝͇̱̥̒͐̏́͋̇͑͛͘͠ų̴̞̥͈͓̦̤̰̞̆̀͆̆͒̃̓͒͒͝͝,̷̛̖͕̞̱̬̯̣͍̦̄͂͊ ̶̢̢̛̛̣͈̬̤͎̜̭̯͍̊͋̓̈́̆̃̅̉̈́̌͜͜d̵̡̙͎̰̏̈́̈́́̋̊͝͝ǫ̷̠̥̝͓̦͌͋̉̀̏n̷̠̦͎̬̽͂̂͌̊̓̕͝ṫ̸̢̪͙̭̮̬̜̈̂̈́ ̴̭̣̥̙͙̫͓͇̖̣̲͋̔͆̂́́͊̔̀́̀̾͜͝d̵̨̨̧̳̞̰̣̞̐͊̔͂̔̽͗͋ͅó̶̥̝̺͇ ̴̡̪̦̳͕̻͎̈́͒̈̊̊͒̇̕̚͝ť̸̜͖̃̋̈́͜ͅh̷̛̞͔͚̹̫̫̞̼̦̰͓͛̂̿͆̋̀͛̚i̵̢̙̅̏̄͗̃̾̍̊̄̿̌̑̾ş̵̛̜͔͇͚͌̐̔͂̎̽͂̕̕͝͝͠", fast )
                        intro_boss += 1
                        return pvm(0)
                        
                    elif response.lower() in run:
                        echo_dialogue( "n̶̓̇͗ͅ4̴͉̞̠̕9̶̡̅̈̄̀ḑ̶͇̻̈͆̇a̷̩̺̐͛͌͌ŝ̸̜̮̲͌" )

                    else:
                        echo_dialogue( "Ṛ̷̢͇̣͕̈́̐̾E̵̩̹̼̭͆́̉D̶̛̺̗̭̘̘Ą̸̖͓̜͓͛͆̇̆͑C̵̩͇̙̈́́̀̓T̷͔̦̔Ę̶̧͇̣͠D̶͙̤͛͑͆͒" )

            elif response.lower() in carriage_loc:
                echo_dialogue( "I̸t̴'̶s̶ ̸t̷o̴o̷ ̶l̶a̵t̵e̸ ̷f̵o̶r̵ ̴y̴o̴u̶" )
            
            else:
                echo_dialogue( "Ṛ̷̢͇̣͕̈́̐̾E̵̩̹̼̭͆́̉D̶̛̺̗̭̘̘Ą̸̖͓̜͓͛͆̇̆͑C̵̩͇̙̈́́̀̓T̷͔̦̔Ę̶̧͇̣͠D̶͙̤͛͑͆͒" )

# Forest Level
def forest():

    global player_name
    global player_class
    global intro_boss
    global foot_prints
    global bear_tracks
    global follow_prints
    global follow_tracks

    forest_art()

    if crash == True:
        while True:
            echo_dialogue( "* Inside the thick dark forest, you hear the call of crows and wolves echoing through the trees." )
            echo_dialogue( f"* You notice {human_bear()} on the ground." )
            
            echo( "[===========================================]", fast )
            echo( "[ What would you like to do ?               ]", fast )
            echo( "[ 1. Look around.                           ]", fast )
            if intro_boss == 2:
                echo( f"{foot_prints}", fast )
            else:
                echo( f"{bear_tracks}", fast )
            echo( "[ 3. Return to the carriage.                ]", fast )
            echo( "[===========================================]", fast )
            response = input( "1. / 2. / 3. : " )
            
            if intro_boss == 2 and response.lower() in follow_prints:
                echo_dialogue( "* You decide to follow the prints." )
                if intro_boss == 2:
                        while True:
                            echo_dialogue( "* As you follow the tracks, you come to a clearing and stop." )
                            echo_dialogue( "* There's a body on the ground...", slow )
                            time.sleep(3)
                            echo( "[===========================================]", med )
                            echo( "[ What would you like to do ?               ]", med )
                            echo( "[ 1. Leave.                                 ]", med )
                            echo( "[ 1. L̸̮̿e̷̝̅à̸͉v̸͔̓e̵͙͘                                  ]", fast )
                            echo( "[ 3. Investigate.                           ]", slow )
                            echo( "[ 1. Leave.                                 ]", med )
                            echo( "[ 1. L̵̡̾e̴̹͚̽͊ă̶̢̩̰͔̒v̵͓͇͓̀͝è̶̡̠͚                                 ]", fast )
                            echo( "[ 1. Leave.                                 ]", med )
                            echo( "[ 1. L̸̰͠e̶̖͠a̴͓͑v̸̩̍e̷͙̋                                  ]", fast )
                            echo( "[ 2. Leave.                                 ]", fast )
                            echo( "[===========================================]", med )
                            response = input( "Y̷̫͂ő̴̲̦͛u̷̱̇̋̓ͅ'̷̧̏͒ṛ̴̦̈͘͠e̴̜͍͗͜͝ ̵̟̈́̒͝ṛ̶̗̑̒̂ǘ̸͓̃̊i̵͈͚͙̓͌͠ň̷͍͔͠i̵̫̣̝̾n̷̟̤̲̄g̶̮̺̿̈́ ̶͕͌͐͒e̸̟̝̿̒̀v̷̤̙̒́ě̶͙̺̏̉r̶͔͑y̸̛̰͍͖t̷̰͐̈͌h̷͎̘͖̆i̴̧̛͂̕n̶̟͙̅g̶͖̋ : " )

                            if response.lower() in investigate:
                                echo_dialogue( "* You carefully walk towards the body on the ground." )
                                time.sleep(2)
                                echo_dialogue( f"* The body of a {class_list[player_class]} lies in the centre of the clearing." )
                                echo_dialogue( f"* You approach the body of the {class_list[player_class]}; turning the body over you see they have no face - just skin." )
                                echo_dialogue( "...",slow )
                                time.sleep(2)
                                echo_dialogue( "* You decide it's time to leave." )
                                break

                            else:
                                echo_dialogue( "* You leave the clearing without looking back." )
                                break

            elif response.lower() in follow_tracks:
                while True:
                    echo_dialogue( "* You decide to follow the bear tracks." )
                    echo_dialogue( "* As you follow the tracks, you come to a clearing and walk into the center." )
                    echo_dialogue( "* All the sudden a great bear walks out of the tree line, and locks eyes with you.", fast )
                    echo_dialogue( "* Standing tall on its back legs, the bear roars - causing brids and small wildlife to flee." )
                    echo( "[===========================================]", fast )
                    echo( "[ What would you like to do ?               ]", fast )
                    echo( "[ 1. Fight.                                 ]", fast )
                    echo( "[ 2. Run.                                   ]", fast )
                    echo( "[===========================================]", fast )
                    response = input( "1. / 2. : " )
                                
                    if response.lower() in fight:
                        bear_art()
                        return pvm(1) # PvM code
                                
                    elif response.lower() in run:
                        echo_dialogue( "* You run from the bear and leave the clearing." ) # calls the player a pussy
                        break

                    else:
                        echo_dialogue( "Not an option" )
            
            elif response.lower() in look_around:
                echo_dialogue( "* You scan the area - lush trees overhead block out the sunlight, making the forest dim.", fast )
                echo_dialogue( "* Every now and then you manage to catch the occassional small animal watching you from afar; this is their home and you're an uninvited guest.", fast )
                echo_dialogue( "* As with all things, curiosity wins out and they can't help coming to investigate this new being.", fast )
                echo_dialogue( "* You see their beedy eyes glimer in the distance - some would call this peaceful, others would say otherwise.", fast )
                echo_dialogue( "* We live in a society.", fast )

                echo_dialogue( "* You return your attention back to the path." )
                

            elif response.lower() in carriage_loc:
                echo_dialogue( "* You begin your walk down the forest path, back to the carriage." )
                return carriage()
            
            else:
                echo_dialogue( "Not an option." )
    
    else:
        echo_dialogue( "* As you walk into a thick dark forest, you think you can hear the call of crows and wolves echoing through the trees - but they don't sound right." )
        
        echo_dialogue( "* There's also something else, it also sounds liI̶̝̪̤̮̒̈̓́̾T̵̡̢͍̖̮͙̝̼͒͒̅S̵̢͓̖̯̜̬̤͍̱̺̑̂́͛̚̕͜ ̷͕̮̻̈́̀͠Ğ̴̞͎̽E̸̢͙̰̳͚̒̉͐͗̀̇̾̿̓T̵̹͔͔̻͊̈͂̌͊Ḡ̶͉̣͓̞̹̣͔̿͌̆̆̀̒͗͗̔̑ ̴̤͉̃̈̾̈͑̉̀̔͗̚Ĉ̷̨̩͚̌̈́̕L̴͎̺̓́́͝S̴̡̜̋͌͋̌̅͐͑̕͝͝͝E̷͓͙̔̃̈́̀̃́̿̉͠Ŗ̸̡̢̦̭̞̗͕̖͙̼̑̈́̋͂̿̊̋̽́͑͆", fast)
        
        echo_dialogue( "* You notice what look like bear tracks on the ground." )
        
        while True:
            echo("[===========================================]", fast)
            echo("[ What would you like to do ?               ]", fast)
            echo("[ 1. Look around.                           ]", fast)
            echo("[ 2. Follow the tracks.                     ]", fast)
            echo("[ 3. Return to the carriage.                ]", fast)
            echo("[===========================================]", fast)
            response = input( "1. / 2. / 3. : " )
            
            if response.lower() in look_around:
                echo_dialogue( "* ḏ̷̥̑̽͐̽s̵͔̏̆n̶̓̇͗ͅ4̴͉̞̠̕9̶̡̅̈̄̀ḑ̶͇̻̈͆̇a̷̩̺̐͛͌͌ŝ̸̜̮̲͌d̶̥̂̈́.", fast )
            
            elif response.lower() in follow_tracks:
                echo_dialogue( "* You decide to follow the bear tracks" )
                while True:
                    echo_dialogue( "* You decide to follow the bear tracks." )
                    echo_dialogue( "* As you follow the tracks, you come to a clearing and walk into the center." )
                    echo_dialogue( "* All the sudden a Great Bear walks out of the tree line and locks eyes with you, t̷̗͉̀̈̿͆̅ḩ̵̙̳͔͍͒ę̴͖̬̬͖̃͒̈̀̒̽ ̸̻̙̜̱̲̐͝͠e̸̗̭͉͍̝̯̽͐y̶̬̑͝ě̷̗̱̣̮̋͑̊̂͝ŝ̵̫͖͍̼͇̫ ̴͎͗̍͐̆͠a̷͔̬̖̍̉̾̌r̴̘̙̦͂̿̂e̷͚̐̆̄͛̑͝ ̸̛̞̝̞̪̹̓͐̓̑̕b̶̹̾͐̂͐l̷̛̖̈͑͗͊̚e̶̗͙̟͝d̶͓̠͓͎̫̈̓d̸͚̼̖̒̂͆̋͝į̴̖̲̯̓̋̇́ǹ̷̹̗̬͘͜g̸͖̫̮̊̑̌͆͘͠.", fast )
                    echo_dialogue( "* Standing tall on it's back legs, the bear ḏ̷̥̑̽͐̽s̵͔̏̆n̶̓̇͗ͅ4̴͉̞̠̕9̶̡̅̈̄̀ḑ̶͇̻̈͆̇a̷̩̺̐͛͌͌ŝ̸̜̮̲͌d̶̥̂̈́." )
                    echo( "[===========================================]", fast )
                    echo( "[ What would you like to do ?               ]", fast )
                    echo( "[ 1. Fight.                                 ]", fast )
                    echo( "[ 2. Run.                                   ]", fast )
                    echo( "[===========================================]", fast )
                    response = input( "1. / 2. : " )
                                
                    if response.lower() in fight:
                        bear_art()
                        echo_dialogue( "Great Bear: p̷̫̫̀̂l̸̳̏e̶̺̅̂̈̕a̶̝̙̥͈̫͑̎s̴̲͇̳̙͗́̒͜ȩ̶̘̳̦̮̀̒̿̀͐͝ ̵͙͕̿̃̄͆̄͐d̷̨͓̋o̶̢̩̫̭͚͗́̚̚͝ṋ̷̭̰̈́ͅt̸̛̩̹̣͆̉̾ ̵̲̖̯̱̍d̵̗̥̲̿̈́̓̀͘o̸̧͎̮͍͕͝ ̷̝̲̝̰͐͛͛̈̍̚t̴̖̜̣̰̪̍̀̾̐͝ͅḩ̶͖͖̪̯̼̂ï̴͍͙̪̼̟͎͛́̌̂s̸̛̘̥͓̞͈̄̌̄̌͛", fast )
                        intro_boss += 2
                        return pvm(1) # placeholder for the PvM code
                                
                    elif response.lower() in run:
                        echo_dialogue( "n̶̓̇͗ͅ4̴͉̞̠̕9̶̡̅̈̄̀ḑ̶͇̻̈͆̇a̷̩̺̐͛͌͌ŝ̸̜̮̲͌" )

                    else:
                        echo_dialogue( "Not an option." )

            elif response.lower() in carriage_loc:
                echo_dialogue( "I̸t̴'̶s̶ ̸t̷o̴o̷ ̶l̶a̵t̵e̸ ̷f̵o̶r̵ ̴y̴o̴u̶" )
            
            else:
                echo_dialogue( "Not an option" )

# Post-intro game code

# Village Level
def village():

    global player_name
    global player_class

    village_art()

    echo_dialogue( f"* You head into the village centre and look around. There's a shop, a man sitting on a carriage, a tavern - and not much else. " ) # Village description
    
    while True:
        echo( "[===========================================]", fast )
        echo( "[ What would you like to do ?               ]", fast )
        echo( "[ 1. Go to the shop.                        ]", fast )
        echo( "[ 2. Visit the Tavern.                      ]", fast )
        echo( "[ 3. Speak to the man on the Carriage.      ]", fast )
        echo( "[===========================================]", fast )
        response = input( "1. / 2. / 3. : " ) # Player choice
        
        if response.lower() in shop_loc:
            echo_dialogue( "* You head towards a shop that sits in the village center." )
            return go_shop()

        elif response.lower() in tavern_loc:
                echo_dialogue( "* You make your way over to the tavern." )
                return go_tavern()

        elif response.lower() in carriage_loc:
                echo_dialogue( "* You approach the man on the carriage." )
                return carriage()

        else:
            echo_dialogue( "Not an option" )

# mountain
def mountain():

    global player_name
    global player_class

    echo_dialogue( "" )
    while True:
        echo( "[===========================================]", fast )
        echo( "[ What would you like to do ?               ]", fast )
        echo( "[ 1. Look around.                           ]", fast )
        echo( "[ 2. Go into the Dragons lair.              ]", fast )
        echo( "[ 3. Return to the Carriage.                ]", fast )
        echo( "[===========================================]", fast )
        response = input( "1. / 2. / 3. : " )
        
        if response.lower() in look_around:
            echo_dialogue( "* Half way up is still a long way down. Up this high on the mountain you can see most of the realm.")
            echo_dialogue( "* Even the Tower, surrounded by its storm, is visible from here." )
            echo_dialogue( "* The wind hits you hard and relentlessly up here, but the view almost makes you forget about it - it's breathtaking." )
            echo_dialogue( "* You see now why the dragon chose this place.")
        
        elif response.lower():
            echo_dialogue( "* You decide to head into the Dragon's lair, hoping to catch it off gaurd." )
            echo_dialogue( "* The dragon is currently deep into one of it's 100 year long sleep cycles - this would be the perfect opportunity to strike.")
            echo_dialogue( "* Or so you thought, until you kick a rock into the endless pile of gold... and the dragon beings moving.")
            echo_dialogue( "Dragon: Who has come to disturb me?")
            echo_dialogue( "Dragon: Come to steal from me perhaps?")
            time.sleep(1)
            echo_dialogue( "Dragon: Oh, you're a Slayer?" )
            echo_dialogue( "Dragon: No? Not yet... you haven't earned your title yet AHAHAHAHA!" )
            echo_dialogue( "Dragon: THEY REALLY THOUGHT SOMEONE LIKE YOU COULD KILL ME?!" )
            echo_dialogue( f"Dragon: Oh my, I'm almost insulted, you think you have what it takes {player_name} the {player_class}?" )
            echo_dialogue( "Dragon: In any case, lets find out..." )
            dragon_art()

            return pvm(2)
            


        elif response.lower() in carriage_loc:
            echo_dialogue( "* Carefully you hike back down the mountain, back to the carriage." )
        
        else:
            echo_dialogue( "Not an option." )

# necromancers tower
def necromancers_tower():

    global player_name
    global player_class

    echo_dialogue( f"Jimmy: You're either crazy, or I should be a lot more scared of you, {player_name}.")
    echo_dialogue( "Jimmy: I'll be waiting here in case you change your mind - don't go getting yourself killed." )
    echo_dialogue( "* Despite the warning from Jimmy, you head towards the tower." )
    necrotower_art()
    echo_dialogue( "* The rightfully infamous Dark Tower of the Necromancer - once you enter, there's no turning back." )
    echo_dialogue( "[!!WARNING!! - !!YOU CAN NOT LEAVE THE TOWER ONCE YOU ENTER!!]" )

    while True:
        echo( "[===========================================]", fast )
        echo( "[ What would you like to do ?               ]", fast )
        echo( "[ 1. Look around.                           ]", fast )
        echo( "[ 2. !Enter the Tower!                      ]", fast )
        echo( "[ 3. Return to the Carriage.                ]", fast )
        echo( "[===========================================]", fast )
        response = input( "1. / 2. / 3. : " )

        if response.lower() in look_around:
            echo_dialogue( "* Looking up, your mind can't process how big the tower is. Stone as black as the night crashing into the sky." )
            echo_dialogue( "* The top, glowing with red, clouds circling around it - angry like a rabid animal trying to break free from its cage." )
            echo_dialogue( "* Lighting and blood red flashes strike out from the eye of the storm." )
            echo_dialogue( "* The heat is so intense at the base of the tower, you have to shield your face from it." )
            echo_dialogue( "* The ground is scorched so badly that no fauna grows here, and parts of the ground are molten." )
            echo_dialogue( "* Whatever awaits for you inside will be unlike anything you've faced before." )
            echo_dialogue( "* You feel it deep in your gut that if you enter, you may not leave here alive..." )

        elif response.lower() in enter_nectow:
            while True:
                echo_dialogue( "[!!!THIS IS YOUR FINAL WARNING!!! !!!ONCE YOU ENTER YOU CANNOT LEAVE!!!]", slow )
                echo( "[ ARE YOU SURE YOU WISH TO ENTER ?]", fast )
                response = input( "[           YES OR NO             ]: " )
                if "yes" in response.lower():
                    echo( "* Aware of what awaits, you cautiously enter the tower.", med )
                    echo( "* Every step you take, every second, you're blasted with heat and wind.", med )
                    echo( "* But you push on, you have to - this is where your prove yourself to be worthy to be called a Slayer; this is where you really fight.", med )
                    echo_dialogue( "* Here you make history, or die trying, your moment for all of time." )
                    time.sleep(1)
                    echo_dialogue( f"* Steady yourself, {player_name} the great {player_class}..." )
                    time.sleep(1)
                    echo_dialogue( "Mysterious voice: I've been waiting.", slow )
                    time.sleep(1)
                    echo("*You reach the doors finally, they open on their own, but this doesn't distract you, this is a powerful magical tower afterall, that you have to climb to the top of.")
                    echo("*You begin you ascent up the winding stairs, cutting down skeleton soldiers as they charge you, level by level, you finally make it.")
                    echo_dialogue("Necromancer: You DARE enter MY TOWER, you, YOU of all beings think you can kill me?")
                    echo_dialogue(f"Necromancer: You'll make a nice addition to my army {player_class}.")
                    necrofight_art()
                    return pvm(3)

                elif "no" in response.lower():
                    echo_dialogue( "* You turn away; you're not ready for what lies ahead." )
                    echo_dialogue( "* You journey through the wasteland surrounding the tower, back to the carriage." )
                    return carriage()

                else:
                    echo_dialogue( "YES OR NO" )
            
        elif response.lower() in carriage_loc:
            echo_dialogue( "* Heading away from the looming dark tower, you make your way back to the carriage." )
            return carriage()
        
        else:
            echo_dialogue( "Not an option." )

# Swamp Location Function
def swamp():
    global player_name
    global player_class

    swamp_art()

    echo("\x1B[3m"+"The eery mists on the swamp make it difficult to make out anything, you follow the compass south-wards.\n"+"\x1B[0m")
    echo("\x1B[3m"+"There’s an un-easy feeling that runs through you.\n\n"+"\x1B[0m",0.07)
    echo("\x1B[3m"+"Maybe this was a bad idea...\n\n"+"\x1B[0m",0.07)
    time.sleep(0.7)
    echo("\x1B[3m"+"Maybe you should go back?\n"+"\x1B[0m",0.1)

    response = input("Turn back?  ")
    if response == "yes":
        echo("\x1B[3m"+"Good choice...\n"+"\x1B[0m",0.14)
        return carriage()
    else:
        echo("\x1B[3m"+"...\n"+"\x1B[0m",0.1)
        time.sleep(0.4)
        return witch_riddle()


# Carriage/Travel Function
def carriage():

    global jimmy_greeted
    global player_name
    global player_class

    jimmy_art()

    while True:
        if jimmy_greeted == 0:
            
            echo_dialogue( "Jimmy: Hey why'd yo...", fast )
            time.sleep(1)
            echo_dialogue( "Jimmy: Never mind." )
            echo_dialogue( "Jimmy: I mistook you for someone else." )
            echo_dialogue( f"Jimmy: Anyways, I'm Jimmy - guessing you're one of them {class_list[player_class]}'s right? I can take you where you need to go." )

            echo_dialogue( "Jimmy: There's a cave off west known to be the home to a giant rat, should be easy enough for you to handle.", fast )
            echo_dialogue( "Jimmy: The forest with a great bear that roams through it to north east, as well as the swamp, home to the witch and other things.", fast )
            echo_dialogue( "Jimmy: To the north west, the mountain, said to be hiding a dragon's lair high up on its cliffs - you best tread carefully around there.", fast )
            echo_dialogue( "Jimmy: Lastly, the Necromancer's tower to east, although I'll warn you now - you're best off staying away from there if you know whats good for you.", fast )
            jimmy_greeted += 1

        else: 
            echo( "[===========================================]", fast )
            echo( "[ Jimmy: So, where we off to?               ]", fast )
            echo( "[ 1. Village.                               ]", fast )
            echo( "[ 2. Cave.                                  ]", fast )
            echo( "[ 3. Forest.                                ]", fast )
            echo( "[ 4. Swamp.                                 ]", fast )
            echo( "[ 5. Mountain.                              ]", fast )
            echo( "[ 6. Necromancers Tower.                    ]", fast )
            echo( "[                                           ]", fast )
            echo( "[ 7. Information on locations.              ]", fast )
            echo( "[===========================================]", fast )
            response = input( "1. / 2. / 3. / 4. / 5. / 6. / 7. : " )
            
            if  response.lower() in cave_loc:
                return cave()

            elif response.lower() in forest_loc:
                return forest()

            elif  response.lower() in village_loc:
                return village()

            elif response.lower() in swamp_loc:
                echo_dialogue( "Jimmy: Oh… so you wish to go to the swamp?" )
                echo_dialogue( "Jimmy: Thats beyond my travels, I wouldn’t want to head there anyways." )
                echo_dialogue( "Jimmy: You’ll have to figure out your own way - it’s directly south. Here, take this." )
                echo_dialogue( "Jimmy passes you a compass. You notice the rowboat, and know it’s time to start your journey." )
                return swamp

            elif  response.lower() in mountain_loc:
                return mountain

            elif response.lower() in necro_loc:
                echo_dialogue( "Jimmy: You better be sure about this." )
                return necromancers_tower()

            elif response.lower() in loc_info:
                echo_dialogue( "Jimmy: There's a Cave off west known to be the home to a giant rat, should be easy enough for you to handle.", fast )
                echo_dialogue( "Jimmy: The Forest with a Great Bear that roams through it to north east, as well as the Swamp, home to the Witch and other things.", fast )
                echo_dialogue( "Jimmy: To the north west, the Mountain, said to be hiding a Dragons lair high up on it's cliffs, you best tred carefully around there.", fast )
                echo_dialogue( "Jimmy: Lastly, the Necromancers Tower to east, although I'll warn you now, you're best off tstaying away from there if you know whats good for you.", fast )

            else:
                echo_dialogue( "Jimmy: I don't understand what you mean by that." ) 

# art section

def necrotower_art():
    echo( '''⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⡉⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⣿⣿⣿⣿⣷⣾⣿⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣄⣉⣙⡛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣬⣉⣉⠙⠻⠿⠏⢹⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⡉⠛⠻⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣈⠙⠏
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣉⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣤⣤⣄⡉⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣄⣉⡙⠛⠛⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣤⣈⣉⠙⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢉⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣈⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⡈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⡇⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⣉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣀⣦⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣁⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣃⣸⣿⣿⣿⣿⡿⠋⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠀⢀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠘⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢻⣿⣿⣿⣿⠏⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣎⣹⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢁⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠲⠦⢾⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠰⡖⠂⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠠⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⠀⠀⠀⠤⣶⣤⣤⣤⣤⣬⣉⡙⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣧⣼⣷⣶⣿⣿⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣄⣽⣛⠛⢻⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢲⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣾⣿⣿⣿⣿⣿⣿⣿⣏⠀⡖⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠧⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠛⠛⢛⣻⣿⣿⠀⠀⠀⠉⣿⣿⣿⡟⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡶⢤⣄⡈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠰⠿⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⣁⣤⣾⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣀⣻⣿⣿⣿⣶⣦⣤⣤⣈⠙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠈⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⠀⠴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣀⣤⣾⣿⣿⣿⣿⣿⣿⣧⣼⣿⡏⠀⡀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠸⣿⣿⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣿⣿⣿⣷⣶⣄⠉⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢀⣾⣿⣿⣿⣿⣿⣿⣿⡟⢻⣿⣿⣿⠄⠀⡇⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⣈⣹⣷⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⣿⣿⣿⣿⣿⣿⣿⠟⢛⣁⣸⣿⣿⣿⠀⠀⡇⠀⠀⣸⣿⣿⣿⣿⣿⠛⡏⢹⣿⣿⣿⣿⣿⣇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⣠⣿⣿⣧⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣼⢻⣿⣿⣿⣿⠋⣠⢶⣿⠈⣙⡻⣿⡏⠀⠀⢠⠀⣀⣿⣿⣿⣿⣿⣿⣿⡇⠈⣿⣿⣿⣿⣿⣿⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣹⣶⣶⣿⣿⣿⣿⣿⣧⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣿⣿⣶⣶⣄⡈⠙⠻⢿⠿⣿⣿⣿⡄⠙⣿⣿⣿⣿⣿⣤⣿⣾⣿⣄⣀⠁⣹⡇⠀⠀⠘⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⡿⢿⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣶⣤⣿⣶⣶⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣼⣿⡇⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣠⣿⠟⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣧⡸⢿⣀⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⠧⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢱⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⡟⢠⣿⣿⣿⣧⡌⢻⣄⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣧⠈⢿⣿⣿⣿⣿⣧⣾⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⡄⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠀⠀⠃⠀⠀⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠀⠉⠀⠀⢀⡀⠀⠀⠉⠀⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠙⢇⠘⣿⣿⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⣀⠀⠀⠘⠀⡄⠀⠀⠀⠀⠀⠈⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⠿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⡄⠹⢿⣿⣿⣿⠈⢿⣿⣿⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢰⡇⠀⠀⢸⠀⡇⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣼⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠀⠀⠀⢸⠀⡇⠀⠀⠀⠀⠀⡆⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⡎⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢸⠀⡇⠀⠀⠀⠀⠀⠁⢸⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⢻⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠸⠀⠃⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣙⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢻⣿⣿⣿⣿⣿⣿
⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⢀⣀⣼⣿⣿⣿⣿⣧⡈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉⣶⣿⣿⣿⣿⣿⣿⣿
⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⡇⠀⠀⠀⠀⢿⣿⣿⣿⣿⠻⡄⠙⢧⠈⢻⡟⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⡀⢸⣆⣸⣧⡀⣿⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⡇⠀⠀⠀⠀⢸⣿⡀⢿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢰⡇⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠸⠇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣆⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣤⣄⡉⠉⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣸⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⣈⠙⠻⠿⣿⣷⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⠟⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⡉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢠⣧⠀⠀⠀⠀⠀⠘⢻⣿⣿⣿⣿⣿⣿⣿⣿⣧⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣉⡙⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣉⣻⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢠⣿⣿⠆⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣶⣤⣽⣿⡟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠉⠏⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣽⡛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠂⠀⠀⡇⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠂⠀⠀⣧⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢀⠃⠀⢻⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⢈⠀⡐⠀⡸⠀⠀⢸⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠨⠀⢀⠀⠀⠀⠀⢸⡀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣰⢥⠠⠄⠀⠀⠀⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠂⠀⠈⠀⢢⠁⠓⠀⠀⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⡂⠂⠀⢸⡇⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢕⡆⠀⢸⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⠂⠀⠈⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⣷⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠠⡀⠐⠀⠀⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠀⠀⠀⠀⠀⠀⠀⠔⠦⠒⠀⠀⠘⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢀⠤⠀⠀⠀⠀⠀⠀⠁⠀⠀⠘⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⢠⠀⠀⢀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⠀⠀⢀⡐⠂⠄⠀⠀⠀⠀⠀⠀⠀⢸⣿⡆⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢀⠀⠀⡀⠂⠐⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⡎⠀⢀⡂⠠⠠⠀⠀⠀⠀⠀⠀⠀⠀⠰⣉⣷⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠘⡇⠀⠀⠦⠴⠰⣖⣄⡀⠀⠀⠀⠀⠀⠀⣿⣼⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⠁⠘⠃⠀⠀⢠⣴⡖⠓⠿⠤⣤⡄⠀⠀⠀⠀⠛⠻⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⢤⣤⣤⣤⣴⠖⠛⠀⠀⠈⢉⣀⠀⠀⢀⣉⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠼⠁⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠛⠛⠋⠉⠙⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠃⠀⠀⠀⠀⢀⡀⢀⢀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠚⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛
⠰⠲⣆⣴⣶⣀⣿⣏⣉⣉⣉⣉⣉⣹⣿⣿⣉⣉⣉⣉⣿⣍⣿⣿⣿⣿⣿⣉⣿⠿⣿⣿⡿⠿⢿⠿⠟⠻⠿⠛⠛⠿⠿⠿⠛⠛⠟⠻⠿⠀⠤⠟⠃⠘⠛⠻⠟⠛⣿⣷⣶⣿⣧⣌⣭⣿⣿⣧⣄⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣄⣠⣤⣿⣿⣿⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣻⣿⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶
⠒⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣛⣿⣿⣿⣿⣛⣻⣿⣿⣿⡟⠛⠓⠒⠒⠛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣧⣬⣿⣤⣼⣿⣿⣿⣿⣿⣿⣿⣧⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉⣉⣉⣉⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿''', 0.5 )
def forest_art():
    echo('''⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⢸⣿⣿⣿⣿⣿⣿⣿⠇⣴⣿⠏⣹⡟⣻⣿⢉⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⣸
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⢀⣰⣿⣿⣿⣿⣿⣿⣿⠏⣼⣿⣯⣹⡿⣿⣿⢃⣾⣿⢉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⣸⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⢠⣾⣿⣿⣿⣿⣿⣿⣿⠏⣴⣿⣯⣽⡏⣱⡿⢃⣾⣿⢃⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠐⣼⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⣤⣽⣿⣿⣿⣿⣿⣿⣿⠋⣴⣿⣿⣼⡏⣰⣿⢃⣼⣿⢁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⡏⠀⣼⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⠋⣴⣿⡏⣼⡏⣴⡿⢃⣾⣿⢃⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢠⣿⣿⢁⣿⣿⣿⡇⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣴⣿⢿⣿⠟⣼⡿⢡⣼⣿⢃⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣣⣿⣿⠇⣼⣿⣿⣿⠁⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣰⣿⣿⣿⣟⣼⡿⢣⣾⣿⣃⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣾⣿⡏⢠⣿⣿⣿⡏⢰⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣴⣿⣿⣿⢿⣿⣿⢣⣾⣿⣧⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣾⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣼⣿⣿⣿⣿⣾⣿⣿⣿⣿⠏⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣸⣿⣿⣿⡟⢠⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⢿⠿⠿⠿⠿⣿⠿⠿⢿⠿⣿⣿⣿⣿⣿⣿⣿⠿⢿⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢀⣿⣿⣿⣿⠁⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣋⣡⣶⣶⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣶⣦⣍⣙⣻⡿⠋⢁⣴⣽⣿⣶⣬⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣉⡄⣸⣿⣿⣿⣿⣿⣿⣿⣿⢃⣼⣿⣿⣿⠿⣿⣿⠿⣿⣿⡟⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣾⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠿⢻⣛⣿⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣿⣿⣿⣭⡿⠚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣵⣶⣾⣿⣿⣿⣿⣿⣿⣿⣶⣍⣛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⠿⠿⠿⠿⠿⠟⠛⢻⣟⣟⣛⣛⣛⣛⠋⣭⣶⣿⣿⣤⣿⣿⣿⣿⣿⣿⣿⣿⢃⣼⣿⣻⣿⠋⣽⣿⠋⣾⣿⡟⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢰⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⢛⣭⣴⣶⣿⣿⣿⣿⣾⣯⣍⣻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⠿⢿⣿⣭⣷⣷⣿⣶⣶⣬⣉⣛⣛⣛⣋⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣮⣍⡟⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢛⣋⣽⣿⣿⣷⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣼⡿⣿⣿⢁⣾⣿⢁⣾⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢀⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿
⠟⢋⣵⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣶⣿⣷⣮⣍⣛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣉⣤⣶⣦⣈⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⣡⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣿⣿⢋⣿⣿⢁⣾⣿⡟⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣼⣿⣿⣿⣿⡿⢠⣿⣿⣿⣿⣿⣿⣿⣿
⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣌⠛⠿⠛⣛⡛⠛⠛⠻⣿⠿⣿⣿⠿⠛⠉⣤⣤⣍⠻⣿⣿⠏⡀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡜⢻⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣛⡻⠋⢁⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣿⡿⢥⣿⣿⢁⣾⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢰⣿⣿⣿⣿⣿⡇⣸⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣾⣿⣿⣿⣿⣹⣷⡘⠿⠐⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣠⠾⢉⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢡⣿⡟⣿⡿⢣⣾⡿⢁⣿⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⣠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠈⣁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢡⣿⡿⣿⡟⢡⣿⣿⢁⣿⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣸⣿⣿⣿⣿⣿⣿⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢠⣿⣿⣿⡿⢳⣾⡿⢁⣾⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⠏⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣠⣿⢟⣼⡿⢣⣿⡿⢡⣾⣿⡿⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢹⣿⣿⣿⣿⣿⠇⠀⢱⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣰⣿⢟⣼⡟⢰⣿⡿⢡⣾⣿⡟⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣼⣿⣿⣿⣿⡟⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⣿⣿⣿⣿⠇⢀⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣴⣿⢿⣾⡟⣠⣿⡿⢡⣾⣿⡿⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠏⠀⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣴⣿⣿⣾⡟⣰⣿⡿⢁⣾⣿⡿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣿⣿⣿⠿⢿⠿⠛⠟⠛⠻⠛
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢨⣉⣛⡏⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⣾⣿⢿⣿⡟⣰⣿⡿⢁⣾⣿⡿⢡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢸⡿⢁⣿⡿⠛⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣼⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣛⣿⡟⣰⣿⡿⢃⣾⣿⡿⢃⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⡼⠁⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢩⠉⣩⠉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣯⣿⡟⣠⣿⣿⢁⣾⣿⣿⢃⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠙⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢀⣀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢡⣾⣿⣯⣿⡟⣰⣿⣿⠃⣾⣿⣿⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠻⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠉⠀⣤⣤⠀⠉⠉⠀⠀⠈⠉⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⠀⣤⣤⡄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢠⣾⣿⣇⣿⡿⢠⣿⣿⠃⣼⣿⣿⡏⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⠀⠄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠺⣿⣿⣿⣻⡿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣧⣄⠀⠛⠀⠀⠀⠀⠀⠀⠐⣡⣤⣼⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣿⣷⣤⣤⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢡⣾⣿⣇⣼⡿⢠⣿⣿⠃⣼⣿⣿⡏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⡄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⡿⠁⠀⠄⠀⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠁⠀⠀⠈⠉⠛⢿⣿⣿⠆⠘⢻⣿⣿⣿⠛⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠀⠀⠀⠀⠀⡟⣡⠌⠛⠛⢻⣿⣿⣿⣛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢠⣿⣿⣃⣽⡿⢡⣿⣿⡟⣰⣿⣿⡿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⡇⢠⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠋⠀⠀⠀⠀⠀⠀⠈⠚⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⣤⣶⣿⣿⣿⡟⢀⠁⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠻⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⠀⠀⠀⠀⠀⢠⡏⠀⠀⠀⠼⣿⡏⠉⠁⠒⣌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢉⡿⠿⣿⣿⡿⢠⣿⣿⣧⣼⣿⢃⣾⣿⡿⢀⣿⣿⣿⠃⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠀⠀⠀⠀⠉⠁⢸⣿⣿⣿⡇⢸⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠉⠻⠿⢿⣿⣿⣿⣿⣿⡿⠿⠀⢠⣀⠀⠀⠀⠀⠀⠀⠀⠀⢂⣿⣿⣿⣿⣿⠁⡾⠀⠰⣾⡿⢿⣿⣿⣿⠉⢿⣉⣉⠛⠁⠀⠀⠀⠙⠋⠉⠀⠀⠀⢹⣷⣦⠈⠂⠀⠀⠀⠀⡞⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⡌⣷⡮⠉⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋⠉⣴⡏⠀⠀⠀⠀⢀⣿⣿⣏⣹⣿⠇⣼⣉⣉⠁⣾⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⣧⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠬⣿⣿⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢿⣿⣿⣯⣿⠄⠀⣶⠊⠙⠻⢷⣆⡀⠀⠀⠀⠀⣹⣿⡿⢁⡿⠁⠀⠀⠀⠀⠈⠁⠈⠹⣿⣿⠆⠀⢻⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢻⣿⣧⠀⠀⠀⠀⠘⠁⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⡇⣿⣡⠁⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠩⠴⠶⡀⠀⠀⣿⣷⢠⣴⣶⠂⣾⣿⣿⣻⣿⡿⢰⣿⣿⡿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠀⠀⠀⠀⠀⠀⢸⣿⠛⠿⠿⠇⢸⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⢹⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⢻⣷⠀⠀⠀⢀⠀⣰⣤⣤⣉⣿⡆⠀⠀⠙⠀⠀⠀⠀⠈⠉⠳⣶⣶⣾⣿⡯⠄⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠉⠀⠀⠈⠛⢿⡄⠀⠀⠀⠀⠀⠀⢀⣤⣾⢇⠀⠻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠀⠀⢀⣇⣿⠁⢀⣾⣿⣿⣿⣿⠟⠉⠉⠉⢻⣿⣿⣿⢿⣽⣿⣯⣷⡈⢻⣿⣿⣿⣿⣿⣿⠿⡿⣿⣿⡿⠟⠋⠉⠀⢠⣐⣾⡗⣶⠀⢻⣿⢸⣿⡏⣰⣿⣿⠇⣾⣿⠇⣼⣿⣿⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠀⣠⠀⠀⠀⠀⠈⣿⡄⢻⣶⣶⠘⣷
⣀⣀⣀⣀⣀⠠⠀⢀⠀⡀⢀⣾⠃⣼⣿⢻⣧⡄⠀⠀⠀⠀⠀⠀⣾⣿⡆⠀⢀⠀⣼⣿⣿⡏⢹⣿⣷⠀⣄⣀⠀⠀⠀⠀⢀⣀⠠⡈⠻⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⠀⣦⣤⡀⠀⠀⣽⣿⠃⣼⠄⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⡿⠁⠀⠀⠘⣿⡇⠀⣼⣏⠹⡿⠿⠋⠀⠀⠀⠀⡬⠛⠛⠉⠉⢻⣅⠸⣿⣿⣦⡟⢿⡿⣿⡋⢹⠀⠀⠀⠈⠀⠀⠀⠀⠀⢸⠛⣿⠁⣿⡆⢸⣿⠀⠉⠀⣿⣿⡏⢸⣿⡏⢰⣿⣿⡟⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠹⠁⠙⠀⠀⠀⠀⠀⠟⠃⢸⣿⣿⡇⢹
⣿⣿⣿⣿⣿⣶⣷⣾⣤⣴⣿⡟⢰⣿⡇⠘⣿⡇⠀⠀⠀⣤⣾⣀⠉⣿⣇⠈⢻⣼⣿⣿⣿⡇⢸⣿⣿⠀⣿⣿⣤⣤⣤⠸⢿⣿⣇⠀⠀⣠⣤⣤⠀⠀⠀⢠⡿⣹⡇⠀⠀⠀⣴⣶⡆⠀⣤⣤⡄⢠⠘⣿⠘⢿⣿⣿⣷⡶⠛⠁⠀⢸⡇⠋⠀⠀⠀⠀⢰⠀⠀⠀⠀⢸⣿⣿⣧⠀⠀⠀⠀⠛⡇⠀⢻⣿⡆⠀⠀⠀⠀⠀⠀⢀⠀⠀⢠⣀⠀⢸⣿⠀⠀⠀⠈⢁⡀⠀⢨⡇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠀⢿⡇⣼⣿⠀⠀⣾⣿⣿⢃⣿⣿⠃⣾⣿⣿⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠀⣿⠀⠀⠀⠀⠀⠘⣆⠘⣿⣿⣷⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣇⠀⣿⡇⠀⠀⠀⢻⣿⣿⣼⣿⣿⣄⠸⣿⣿⣿⣿⡇⢸⣿⡟⠂⠘⠿⣿⣿⠟⠀⠀⢿⣿⠀⢰⣿⣿⠏⠀⠀⠀⠘⠁⢻⡆⠀⠀⠀⣿⣿⡇⢸⣿⣿⠀⠘⢂⣿⠀⠀⠘⢳⢻⡇⠀⠀⣶⣾⠏⠀⠀⠀⠁⠀⣾⠀⠀⠀⠀⢸⣿⣿⣿⠄⠀⠀⡀⠀⣇⠀⠀⢿⣿⠀⠲⠀⠀⢿⣿⡟⠀⠀⠘⠛⠀⢘⣿⠀⠀⠁⢀⣼⡇⠀⢸⡇⢸⠷⡀⠀⠀⠰⠀⠀⠀⠀⠀⠀⠀⣴⠀⣿⠃⣿⡀⢠⣿⣿⣿⣼⣿⡏⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠋⠀⠀⠀⠀⠀⠀⠺⠀⢻⣿⣿⡇
⡟⠛⠛⠛⠻⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⡆⢻⡇⠀⠀⠀⢸⣿⣿⣿⠃⣤⣤⠀⣼⣿⣿⣿⣯⣽⣿⣿⣼⡄⢀⣈⡉⠙⠀⠐⣿⡇⠀⢸⣿⡟⠀⠀⠀⠀⡄⠀⢘⡇⠀⠀⠀⣿⣿⡇⢸⡀⣿⠀⠀⢀⣿⠀⠀⠀⢹⠀⠁⠀⠀⠛⠏⠀⠀⠀⢰⣶⠀⣿⠀⣤⢄⠀⢸⣿⣿⣿⠀⠀⢀⣿⠀⣿⠀⠀⠘⠃⠀⠀⡆⣴⡘⠟⠀⠀⠀⠀⠀⠃⠈⢻⠀⠀⠀⠸⡏⠀⠀⣾⡇⣿⣦⣵⠈⣿⡟⠀⠀⠀⠀⠀⠀⠀⣽⡇⢻⠀⢿⠃⣼⣿⣿⣿⣿⣿⠇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠘⡃⠀⠀⠀⠀⠀⠀⠀⡇⢘⣿⣿⡇
⣧⠘⠀⣉⡀⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣇⣸⣧⠀⣦⡄⢸⣿⣿⣿⠀⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⠿⢠⣭⣭⡁⠀⠀⠀⣽⠀⠃⣼⡏⠀⠀⠀⠀⠈⠋⠀⢠⡇⠀⠀⠀⣿⣿⡿⠈⠁⣿⠀⠀⣿⣿⠀⠀⡇⢸⠀⠀⠀⠀⡀⠀⠀⠀⣼⣼⣿⢰⣿⡄⢱⣾⡇⢸⣿⣿⣿⡆⣀⣾⣿⠀⡟⠀⠀⢸⡇⠀⠀⢃⣻⠧⠀⠀⠀⢰⠀⠀⠠⠀⢸⠀⢠⠀⡆⠁⠀⠀⢼⡆⢿⠀⢿⣦⠙⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢸⠀⠈⢰⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠃⠀⠀⠀⠀⠀⠀⠀⣿⠈⣿⣿⠇
⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⠃⣿⣿⣿⠁⢸⡟⠀⣥⠒⣸⣿⣿⣿⠀⣿⡇⢠⣿⣿⣿⠟⢉⠎⠉⠀⠀⢸⣿⣿⠁⠀⠀⠀⠁⢨⠐⣻⠁⠀⠀⠀⠀⣄⣻⠀⠀⣧⠀⠀⠀⠿⠟⠁⠀⠀⠘⠀⠀⢿⣿⡀⠰⠃⠈⡄⠆⠀⢀⡀⣶⡆⢰⣿⣿⣿⠀⣿⠃⢸⣿⣿⠸⣿⣿⣿⡇⣿⣿⣿⠀⠁⠀⢠⣿⣷⡄⠀⠘⢿⠀⡀⠀⠀⠀⠀⠀⠀⠀⢰⠀⠈⠀⠃⣰⡄⠀⠈⢷⣈⠀⠀⠉⠁⠀⠀⠀⠀⡆⠀⠀⠀⢸⡇⣿⠀⠀⣿⣿⣿⣿⣿⣿⡇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⣼⣿⢸⣿⣿⠀
⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⠛⡇⢈⣿⣿⡄⣸⣧⣦⣿⣆⢹⣿⣿⠏⣰⣿⠃⠎⠁⡸⠃⠀⠀⠀⢀⠀⠀⣤⣴⣶⠀⠀⠆⠀⠀⠠⣼⣏⠀⠀⠀⠀⠀⢸⣿⠀⠀⠘⠀⠀⠀⠀⠀⠁⠀⠀⠀⡀⠀⠀⠹⣷⡀⠀⠀⠰⡆⠀⣸⣿⣷⣷⣿⣽⣿⣿⣶⣿⣦⣿⣿⣿⡆⢹⣿⡟⠃⢹⣿⣿⡷⠀⢀⢸⡿⢿⣿⡆⠀⠈⢀⠀⠀⠀⠀⠰⠀⠀⠀⢸⡀⠀⠀⣼⣿⡇⠀⠀⠈⠻⣄⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡃⢿⠀⢠⣿⣿⣿⣿⣿⣿⣩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⢿⣿⣾⣿⣿⡄
⣿⣿⣿⣿⣿⣿⣿⣿⡈⣿⣿⣿⡿⠿⣿⣿⡿⢿⣿⣿⡟⣿⣿⡿⠀⣿⣿⠀⢰⣾⣁⣤⣀⠀⢰⠋⠂⠀⠘⠻⣿⡶⠂⢰⡆⠀⠀⢹⣿⠀⠀⠀⠀⠀⠀⠇⢠⠀⠀⠀⠀⠀⠈⢠⣶⡆⠀⠀⣿⠀⠀⠀⠈⠑⢄⠀⣀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣏⠀⡤⢤⠄⣿⣿⡈⠿⢁⡆⢸⣿⣿⠀⣀⡚⢸⣿⣿⡟⠀⠀⠀⠎⠃⠀⠀⠀⠀⠀⡀⢰⣾⡇⠀⠸⣿⣿⠇⢰⣆⠀⠀⠈⣷⠈⣗⠀⠀⠀⠀⠀⠃⠀⠀⠀⢠⣼⡆⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠁⢸⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⠆⠶⠀⢸⣿⣿⣧⠸⣿⠁⣴⣿⡟⢠⣿⣿⣿⣿⣿⡆⠁⠀⠀⠙⠶⠶⠿⠤⠶⣶⣦⣀⣀⣘⣻⡀⠀⠀⠀⠀⣀⣀⣉⣀⡄⠀⠀⠀⠠⢬⣬⣥⣤⣴⣷⣶⡄⠀⠀⠀⠀⢰⣷⣶⡆⢹⣿⣮⢿⣿⣿⣿⣿⣿⣧⣠⣤⣤⣿⣿⣷⡐⣿⡇⣸⣿⣿⡆⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⠶⠶⠶⠶⣶⣶⠇⣀⠉⠁⢶⣶⣾⣯⣄⣛⠛⠆⠤⠆⠿⠄⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⣀⠈⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⡀⢰⠖⠂⢸⣿⣿⣿⠆⠹⠀⢛⣻⣁⡈⠿⠿⠿⠿⠟⢃⣀⣀⣀⣀⢻⣶⣶⣶⣶⣿⢈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⡿⢾⡏⢹⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠈⣿⣿⠇⣾⢿⣿⠌⣿⣿⣿⣿⣿⣿⣿⡟⠻⠿⠿⠿⠷⠈⠁⣿⣿⣿⡇⢻⣿⣿⣿⣭⣿⣿⣿⡟⣿⣿⣶⣶⣶⣿⣿⣶⣿⣶⣶⣶⣶⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡆⢻⢰⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⢨⣤⣭⠉⠿⠿⠿
⣿⣿⣿⣿⣿⣿⣿⣏⣉⣉⣉⣉⣉⣁⣤⡼⠉⠿⠟⠛⠛⠀⠰⠿⠿⠿⠛⠛⠛⠛⠛⢿⣿⣿⣿⣟⣛⣛⣿⣿⣿⣿⣶⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⢖⣂⣀⣀⣉⣉⣹⣿⣀⣶⣒⣒⣒⣂⣉⣁⣀⣉⣈⣉⣉⣉⣋⣉⣉⣋⣙⣙⣃⣙⣿⣉⣉⣉⣋⣀⣛⠛⢛⡛⢸⣿⣿⣿⣿⣿⣿⣿⣷⣿⠿⠿⠿⣿⣿⣶⣷⣯⣭⣽⣿⣿⣿⣿⣿⣛⣛⣻⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⠀⢹⣿⠷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠈⣿⣿⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣿⣿⣿⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⣋⣩⣥⣶⣶⣾⣿⡿⢛⣋⣉⣭⣭⣿⣾⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣬⡄⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣡⣤⣶⣿⣿⣿⣿⣿⣿⣿⣟⠡⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣥⣹⡿⠿⠿⠿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⠀⣿⣿⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢰⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣍⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣬⡙⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣻⣿⣿⣿⣿⣿⠙⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⠟⢻⠛⠛⠛⡛⠛⠛⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⠀⣿⣿⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠻⣶⣦⣤⣤⣼
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣉⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡿⠿⠿⠟⠛⠛⠿⢿⣿⣿⠉⢤⣤⠤⢤⡤⢤⡌⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⡟⣉⣉⣿⣿⣿⣿⣿⣿⣿⣿⣯⣧⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠉⣉⠛⠛⠛
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢟⢛⣉⣯⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⢋⣉⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣽⣭⣿⣿⣿⣿⣏⣤⣿⣿⣿⣿⣿⣿⣿⠿⢿⡟⠛⠛⠛⠛⠛⠛⠿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠘⢿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⢟⣛⣉⣭⣧⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠟⣋⣉⣭⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠠⠴⠶⣶⠶⡾⠶⠶⠆⣸⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣶⣯⣭⣭⣭⣭⣭⣭⣭⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡈⢿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡿⣿⣟⣹⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣉⣥⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⣿⡿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⠤⠴⠶⠶⠶⠶⠶⠶⠦⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣦⣍⣙⣛⠻⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢻
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣉⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣐⠒⡒⠿⠿⠿⠿⣿⣿⡿⢂⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣁⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣡⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⣩⣽⣤⣼⣿⣿⣶⣶⣶⣶⣦⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⣛⣡⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣤⣭⣥⣤⣤⣤⣤⣧⣼⣧⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿''', 0.5)
def cave_art():
    echo('''⠀⡀⠠⠀⠔⣀⠢⠐⡀⣿⣟⡿⣟⣿⣻⣯⣿⣯⢿⡿⣿⣽⣿⣞⣿⡿⣿⢿⣿⣿⣿⢿⣿⣽⣿⣽⣻⢯⣿⣻⣽⣯⡷⣯⣟⣯⣟⣯⢿⣽⢾⣯⣻⣽⢾⣽⣻⡷⣻⣞⣯⡷⡿⣞⣷⣯⣷⢿⣻⣞⡿⣾⣽⢾⣽⢾⣟⣾⢷⣻⡷⣿⣞⡿⣞⣷⣯⣿⣳⡿⣞⣿⢾⣷⣻⣯⢿⡿⢿⣿⡛⠟⢿⣿⡿⣿⣿⢿⠿⡿⣿⠿⠿⠟⠛⠛⠋⠉⢉⠁⡀⢀⠂⡐⢀⠂⡐⠠⢸⣏
⠀⠄⠡⠘⠠⠄⢂⠁⠄⣿⣾⣽⣟⡷⣟⡿⣮⣷⣿⢿⣛⣷⣛⣽⣯⣿⡝⠿⡾⡷⣿⢯⣿⢾⡷⣟⣿⣻⣟⣯⣟⣯⣟⣿⣻⣏⣿⣻⣟⣿⣻⣟⣿⣻⣟⣿⣻⣟⣿⣻⣿⣽⣟⣿⣯⣷⣟⣿⣟⣻⣽⣻⣽⣻⣟⣿⣽⣻⣟⣿⣽⣟⣻⡿⣟⣯⣟⣟⣿⣽⣻⣟⡿⣽⡿⣿⡿⣿⣿⡍⠀⢀⠀⢀⠠⠀⠀⠀⠀⡠⠄⠀⡀⠀⠐⠌⣒⢍⡎⣛⠼⣡⠄⣀⠈⠐⠀⠁⣸⢼
⠀⠌⠠⢁⠒⡈⠄⠌⡀⣿⡷⠏⠘⢿⡹⣿⡿⣭⢽⣾⡻⣝⣻⣞⣳⡽⣿⣦⢐⠂⠘⠿⣽⢿⣽⢿⣾⣽⢯⣿⡾⣽⣞⣷⣻⣽⢿⣽⢾⣻⠷⣿⣾⣟⡾⣯⣟⣾⣻⢷⣻⣷⣻⢷⣻⢷⣻⡷⣿⡽⣿⣽⢯⡿⣾⣽⣾⣻⣟⡾⣟⡾⣟⣿⡽⣯⣟⣯⣷⣻⣯⢿⣽⣷⢿⣷⣻⣿⠝⠀⠠⠀⠌⢂⠡⢀⣠⠖⢎⡁⣠⢥⡙⢮⡹⣩⡜⢎⠾⣱⢿⣬⣟⡶⢆⣢⠀⡜⣧⠻
⠀⠌⡐⢀⠂⠌⡐⠂⠄⢹⠂⠀⠀⠀⣹⢿⣽⣻⣗⠪⢿⣽⣳⢟⣾⣻⡷⣞⢯⠷⢳⢄⡙⢿⣿⣻⣯⣿⣿⢾⣿⣻⣾⣟⣷⣿⣯⡿⣟⣿⣻⣟⡾⣯⣟⣷⣻⣯⣟⣯⡿⣞⣯⣟⣯⣟⣯⣟⣯⣟⣷⣻⢿⣽⣷⣻⢾⣻⡾⣽⢿⣽⣟⣾⣻⡷⣯⣷⣯⢿⡽⣿⣞⣯⣿⣾⠿⡁⠆⢀⠂⡁⠀⡀⢀⣊⠖⢦⣣⢞⣐⡶⣯⠵⢯⡵⠾⣭⢏⣾⡸⢬⡝⣳⡌⠇⣸⢹⢎⡟
⠀⢂⠐⢠⠈⡰⠀⠍⣀⠀⠀⠀⠀⠀⣿⣞⣽⢯⢻⣭⣧⣾⡭⣟⣶⣿⣭⣿⡀⣿⢶⡔⠹⣀⣈⢻⣿⣽⣯⣿⣿⣻⢷⡿⣯⡿⣷⣿⢿⣻⣷⣿⢿⣿⢾⣿⣽⣷⣻⣷⢿⣯⣷⣯⣟⡾⣟⣾⢷⣻⣾⡽⣟⡾⣾⣽⢿⣳⢿⣻⣟⡾⣟⣾⡷⣿⡷⣿⣯⣿⣟⣷⡿⣿⣿⡛⢴⡉⣄⣀⡀⢤⡶⣝⣳⠞⣿⣳⣛⢯⣏⢿⣭⢿⣺⣙⣻⣞⡟⡶⣟⣺⡽⣭⡟⡰⢭⢛⢮⡝
⠀⠂⠌⣀⠂⠤⠑⠈⡄⠀⠀⠀⠀⠀⠹⠾⢯⣟⠓⠲⠤⢤⣻⠭⣯⢶⠿⢴⡷⣈⡷⣛⣿⢺⢶⣒⠉⠻⣾⣻⣯⣟⣯⡿⣷⣿⢯⡿⣿⢿⣽⢯⣿⣻⢿⣻⣽⣻⣽⣯⣿⡷⣿⡷⣿⣟⡿⣯⣿⣷⣿⣟⣿⣟⣿⢾⣿⣻⣟⣿⣻⣿⣟⡿⣟⡿⣟⣿⡷⣿⢯⣿⣽⡿⡽⢐⡇⠸⢞⣹⣛⣞⣽⣶⣚⣻⠭⣧⡷⣯⣭⣻⣽⣯⣷⣻⣽⣚⣿⡳⣯⢷⣻⡟⣰⡹⣋⠞⡧⢯
⠀⡁⠂⠄⡈⠰⠁⢌⠐⠀⠀⠀⠀⠀⢈⡉⢤⢠⠾⡽⣛⠷⢯⣍⣛⠛⠻⣭⠿⣌⠞⡵⢭⣏⠿⣞⣯⣥⠨⡙⢿⣽⡿⣿⢷⣟⣿⣻⢿⣻⢾⣿⣽⣻⣟⡿⣽⣯⢿⣯⢿⣽⣟⡿⣿⡽⣿⣟⣿⣳⣿⣽⣻⢾⣻⢿⣻⣽⣿⣽⣯⢿⣽⢿⣟⡿⣯⣟⣿⢿⣿⣻⣾⣿⠃⣮⢁⣿⣩⡽⣭⡾⢶⣿⣷⣾⢫⠿⣵⡶⠷⣷⣳⠾⣷⠿⣭⣷⣳⢿⢯⣟⠏⣴⢣⡽⣩⢟⡹⡇
⠀⠄⠡⠈⠄⡑⠈⡄⢊⠀⠀⠀⠀⠀⠀⣖⢮⡽⠚⠱⡭⠽⡞⣞⣝⣳⣖⡒⠳⢮⣑⣪⠸⣾⣙⢷⣻⡼⡧⠲⣤⠛⢿⣿⡿⣿⣷⣿⣿⣿⢿⣿⢾⣯⣿⢿⣻⣽⣻⡿⣿⡾⣯⣟⣿⣟⣿⡽⣿⣽⣻⢷⡿⣟⣿⣟⡿⣽⣳⣿⣭⣿⣾⡿⣿⢿⣽⡿⣽⣿⣳⣿⣿⠏⡜⡆⣼⣻⣵⣟⡽⣵⣿⢻⡶⣯⢿⣿⢷⡾⣟⡻⣿⣻⡻⣿⣭⢟⡿⣿⣿⢋⡼⣣⠟⣜⣣⢏⡷⡍
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢄⠀⡐⠂⠃⠄⠐⡸⢈⠃⢌⡑⠒⣈⠘⠈⠂⠈⡙⠚⠀⠷⠱⡆⠠⠀⠀⠸⣷⢻⣿⣿⣹⣿⢾⣿⢺⣿⣼⣾⢿⢻⣹⣷⢏⡗⣿⡿⣹⣼⢻⣷⢻⢧⣿⡞⣷⢻⣼⣹⣷⢻⣿⣹⡟⣏⣧⣷⡟⡾⣧⣷⣿⢿⣏⣿⡟⠠⡱⢀⣧⢻⡼⣹⠓⣧⡜⣎⣷⡙⢾⣏⢾⡔⣿⣱⣿⣹⣷⢣⣏⡞⡷⡿⠁⣄⢣⡉⢶⢸⢡⠊⡤⡁
⠀⡐⠠⢀⠐⡀⠔⡀⠆⠀⠀⠀⠀⠀⠀⢸⡜⣃⡇⣘⡦⣔⠲⣤⣤⢳⡄⡘⠓⡤⣞⠦⣔⣂⣤⣐⠒⠴⢄⠸⠓⢀⠐⠦⠸⣿⣻⣿⢿⣿⢾⣿⢿⣿⢿⣿⢾⣿⣿⣿⣾⣿⢿⡷⣿⣧⣿⣟⣿⣾⡿⣿⢿⣿⢿⣻⣿⣻⣧⣿⢿⣿⣟⣿⡿⣷⣿⢿⣿⣾⣿⣿⠃⡶⣰⢸⣻⢾⡷⣻⢿⣼⢿⡿⣼⢿⣞⣻⣾⣻⣼⣻⢿⣿⣼⣾⢿⡿⣷⠇⣸⡸⢆⡼⢢⡼⣘⡞⢧⢣
⠀⠄⡁⢂⠂⢡⠂⠔⢈⠀⠀⠀⠀⠀⠀⢨⣛⡵⣛⢧⠞⣭⡹⠴⣭⠱⢚⣀⡒⢅⠶⣚⢳⣴⠂⠀⠄⠀⡀⠁⠀⠜⣡⣀⠢⡙⢿⣽⣿⢿⣻⣟⡿⣯⢿⣿⣻⣿⣽⢯⣿⢯⣿⡿⣟⣿⡿⣟⣿⣻⢿⣟⣿⣽⡿⣟⣿⣽⡿⣾⣿⣻⣾⣿⣿⢿⣫⣿⣿⣿⣿⡏⡸⢡⠇⢸⢾⣛⣷⣯⡿⣟⣿⣽⢿⣿⣻⣭⣿⡽⣿⡽⣷⢾⣾⣿⣯⢿⡟⢠⡳⣝⡫⢞⣥⢳⢳⡚⣣⠷
⠀⢂⠰⠀⠌⡐⠨⠐⡈⠀⠀⠀⠀⠀⠀⠀⣟⡶⠾⢧⠻⡵⠒⠋⣄⡒⣃⠖⣩⠆⣖⠨⠥⣞⣭⡥⢶⡀⣄⠲⡀⠣⣄⣈⠀⣆⢃⠙⠾⣟⣿⣿⣽⣿⣟⣿⣻⣟⣾⣿⢿⡿⣾⢿⡿⣯⢿⣟⣿⡿⣿⣟⣿⣾⣿⢿⣟⣿⣿⣿⢯⣿⣿⢿⣯⣿⣿⣿⣿⣿⣿⢁⡹⢨⠇⣸⣟⣿⣽⣻⣽⡻⣟⣽⡿⣿⣟⣾⣳⣿⣻⢿⣽⣟⣷⣿⣿⠏⡰⣌⢷⡪⢽⣩⢎⢯⡳⣙⢮⡓
⠀⠆⠠⠑⡈⠤⠡⠑⡐⠀⠀⠀⠀⠀⠀⠀⣈⠻⠓⠪⢥⢆⡖⢓⠦⡱⢎⡱⠆⠳⡌⢍⡳⢬⢆⡛⠋⠠⠍⡀⠔⠃⢦⡈⣔⠫⠶⢌⠂⠙⣷⣿⣷⣿⣽⣷⡿⣟⣷⣯⣿⣿⣻⣟⣿⡿⣿⡿⣿⣿⣿⣽⡿⣷⣿⣿⣿⣟⡿⣾⣿⣿⣿⣿⣿⣿⡿⣿⣾⣿⡿⢨⢅⣫⠀⣟⣿⡾⣷⣯⣷⣿⡿⣿⣻⢿⣽⣷⣿⣿⣿⣟⣿⣿⣻⣾⠏⡼⢡⣜⢣⡝⣧⢓⠯⣮⠵⣋⡮⡇
⠀⠌⠄⡑⢀⠢⠑⣈⠠⠁⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠁⠚⠠⠮⢤⠥⢤⠳⢦⣑⠭⣔⡙⢦⠀⡂⠀⠀⠴⣍⡄⡖⣬⠽⠎⠯⢛⡞⠀⠘⣌⢿⣻⣿⣿⣿⡿⣿⣿⣿⣿⡿⣿⣻⣿⣿⣿⣿⣿⣽⣿⣻⣿⣿⣯⣿⣯⣿⣿⣿⣟⣿⣿⣿⣿⣻⣿⣿⣿⣿⡇⡸⢸⡜⠐⢿⣷⣿⣿⣿⣿⣿⢿⣿⣿⣿⡿⣷⠿⢋⣵⡝⣮⢗⣛⡁⠮⡕⢤⢫⣜⢺⡔⣫⢻⣜⡣⡟⣜⡃
⠀⢊⠐⡐⠈⡄⠃⢄⠢⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠶⢈⠅⡲⠬⠅⠊⢘⠛⠜⠢⠄⠖⠀⠖⠳⠒⢈⢮⡝⣦⠫⠌⠓⢆⣀⣒⣀⣙⣊⣻⣿⣾⣟⣿⡿⣿⣳⣿⣿⣟⣿⣟⣿⣿⣯⣿⣿⣿⣟⣿⣽⣷⣿⣿⢿⣾⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⢁⡽⢰⡃⢀⢃⠻⣯⣾⡿⣷⡿⣿⡷⠚⣻⣽⢃⣼⣟⣗⣲⠾⣿⣷⣦⡈⢳⢫⠵⣪⢇⠾⣱⢳⠼⣱⢛⡼⣡
⠀⢂⠐⢠⠁⣂⠡⢂⡐⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⣄⢲⠛⢢⠁⠠⠀⡠⠂⢀⠄⣸⠖⣒⣤⣴⣶⣶⣾⣶⣶⣠⢭⣶⣿⣿⣿⣿⡿⣿⣿⢿⣿⣟⣯⣟⡿⣿⣻⣿⣿⢾⣾⣿⣭⣿⣟⢿⣾⡿⣯⣿⣿⢿⣻⣯⣟⣿⣿⢿⣿⣿⣯⣿⣿⣿⡿⣿⣿⣿⣿⢨⣆⢾⠁⠘⣸⡇⠙⠿⢽⣿⣿⠏⡐⠀⣿⠃⡨⣾⣺⠟⣎⢧⣘⠈⢣⢙⠎⡷⣋⢼⣊⠷⣩⣛⡼⢣⣛⡼⣱
⠀⢂⠁⠢⠐⡀⠆⢂⠔⠀⠀⠀⠀⠀⠀⠀⠀⠈⠚⡩⣫⣟⣀⣠⣐⣀⣡⣤⣶⣾⡿⣿⣿⣾⣿⣟⣛⡹⠷⡾⡝⢸⣿⣿⣷⣿⣻⣟⣿⣿⣟⣿⡽⣟⡿⣿⣽⣻⣷⢿⡿⣽⡿⢿⣻⣛⣟⣳⠟⣿⢏⢻⣿⢿⣷⣿⣿⣾⣿⣿⣿⡿⣷⣿⣿⣿⣿⣿⣿⣿⠰⡖⣫⠀⠂⣟⠆⣸⢻⣖⠆⡍⠠⠐⣯⡝⠀⢩⠷⠍⣀⡼⠒⠆⠁⠂⠀⠰⣍⡞⣆⡏⠾⢥⣣⡝⢧⡹⣜⡱
⠀⠡⢈⠡⠌⡐⠄⡊⠄⠀⠀⠀⠀⠀⠀⠀⠀⣬⣿⣽⣿⣿⣿⣿⣿⣿⣿⠟⣫⣾⣿⣽⣾⣯⣟⣾⣯⣿⣗⢶⣅⢿⣾⣿⢿⣿⣿⣿⣿⣽⣾⡿⣟⣻⣽⣻⣳⣶⡾⣻⡹⢷⣹⣯⢯⣟⡼⣏⡿⣭⣿⢧⡙⣿⣿⣷⣿⣿⣿⣽⣷⣿⣿⣿⣿⢿⣿⣿⣿⣿⡄⣧⠓⠐⢰⣋⠠⢏⣣⣴⣶⠂⠆⠈⢠⣦⠀⢤⠠⡀⠀⠀⠠⠀⠂⠀⠀⡰⡭⣜⠲⣍⡛⡞⣴⡹⢣⡳⣍⠞
⠀⢃⠐⢂⠂⡄⢃⡐⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣷⣻⣿⢟⣫⢶⣿⢿⡿⣽⡟⣷⣯⠿⣷⡿⣾⣿⣻⣮⣳⣮⠻⣿⢿⡷⢿⠾⡷⣝⡾⣹⠶⣯⣝⣯⣽⡽⢷⣽⣯⣷⣿⣻⣯⣿⣟⡽⣷⡻⣯⣿⣮⡻⣿⡿⣿⣿⣿⡿⣟⣿⣿⡿⣿⣿⣿⣿⣿⣧⠘⣡⣴⡶⢠⠾⣝⡻⢙⢿⣶⡶⣴⣸⢷⡀⠀⠁⢈⢡⢴⣾⣷⣶⠪⣄⡳⡭⣜⢻⣬⢫⡝⣦⢛⡵⣳⢩⠞
⠀⠡⠌⡐⡈⠔⠂⡌⠀⠀⠀⠀⠀⠀⠀⢰⣾⣟⣿⣟⣯⡿⣻⣵⢿⣛⣿⢾⣯⢿⣻⢿⡯⣟⣿⣝⣿⣗⣯⣵⣟⣳⡻⣷⢢⡑⠼⣘⣳⡙⢯⣿⣱⢯⣳⡽⢮⣶⢻⢯⣟⣾⡽⣯⣻⢯⣷⢿⢿⣝⣷⡻⣧⡟⣿⣌⢿⣿⣿⣿⣿⣿⣿⣻⣽⣿⣿⣿⡿⢟⣡⣬⢛⣡⣶⣾⢷⡶⠁⠀⠉⠑⠛⠷⣻⣿⢧⣖⣖⢧⠭⣿⡿⠷⣝⣥⠾⠓⠝⡜⣳⢬⡳⡜⣥⢛⡴⢣⡟⢮
⠀⠃⢄⠡⡐⠌⢡⠐⠀⠀⠀⠀⠀⠀⠀⠸⢿⡽⢻⡾⢉⣾⣽⣫⡿⣽⢽⣫⡾⣏⢿⣹⡿⣽⡾⣝⡿⣜⡷⣻⣎⣷⣻⡽⣏⡿⡆⡳⢴⢋⢷⡸⢳⣻⠼⣝⣯⣞⣯⢟⣼⢷⣻⣽⣟⣾⣽⣞⣯⣞⣮⣻⡜⣿⡽⣞⡆⢻⣿⣻⣿⣿⣻⣿⣿⣿⢞⣵⣴⠿⠻⠃⠢⠖⠯⠳⢞⡇⠀⢂⠀⠀⣠⣞⢯⠯⡿⣞⡯⢀⠻⠷⠙⠪⠙⠁⠀⠂⠄⠜⢦⢇⣳⣙⢎⡳⣍⡳⣭⢳
⠀⡁⢂⠰⢁⠘⡠⢉⠀⠀⠀⠀⠀⠀⠀⠸⣀⠙⢟⢰⡿⢿⡼⣯⣟⣳⢯⡷⣝⣯⢻⣧⣟⢾⣽⣫⣟⣭⣟⣧⠿⣜⡷⡝⣯⢿⣱⠈⡌⢛⠢⠝⠣⢝⡳⣟⢧⠿⣜⡯⢯⡿⣿⣽⣿⣻⣟⣾⢯⡽⡞⣷⣻⣳⢿⣻⡿⣦⠻⣿⣟⣿⣿⣿⣿⡅⠘⠂⠄⡈⠀⠀⣠⣴⣿⣶⣮⠡⠀⣠⣌⢸⠙⢯⠛⠛⠙⡩⠙⠂⠀⢐⠀⠤⢀⠀⠀⠂⢠⠻⣜⠺⣔⠭⣞⡱⢎⡵⣣⢏
⠀⡡⠌⠰⢈⡐⢡⠂⠀⠀⠀⠀⠀⠀⠀⠀⢄⠈⣀⡼⣍⣻⣚⡷⢾⡭⣟⡼⣝⢮⡳⣕⡾⣽⣲⡻⣾⣝⡾⣼⣻⡝⣶⡛⣽⡞⢧⡇⠀⠠⠓⡌⠲⣌⢖⣈⢿⣻⢮⣟⣿⣻⣳⣟⣾⣳⠿⣏⣾⡱⢯⣯⢯⡽⣯⣳⢿⣭⢷⣨⢿⣿⣯⣿⣻⣇⡀⠀⠀⠀⢀⡾⣽⣟⣯⣿⣯⠪⢆⠁⠙⠀⠀⢀⠀⠀⠀⡀⢆⠂⠄⠁⢈⣀⣤⣘⠐⠀⠍⡳⣜⠹⡼⡸⢶⡙⢮⡵⢣⡏
⠐⠠⠌⣁⠂⢌⠐⡂⠀⠀⠀⠀⠀⠀⠀⠀⢠⢞⠳⡜⣧⢷⡹⣞⠧⢯⡳⣝⢮⡳⣽⢎⣳⣎⠷⣻⣥⣟⣽⣳⢧⣟⣲⣛⡧⣟⡻⣖⠀⠀⠀⠈⡐⣈⠚⡵⣆⡙⠻⡾⣷⣯⣷⣮⢧⣣⣿⣜⡶⣽⣻⣞⣯⢽⣺⣭⣿⢞⣧⣿⡻⡾⢿⡿⣿⣍⠻⣿⣴⣶⠈⣧⣩⠯⠞⠉⠀⠋⠐⠀⠀⠂⠀⠀⠀⠈⠑⠈⠀⣀⣰⣶⣿⣿⣾⣍⣣⣂⣉⡓⢬⢓⣱⠹⢦⢻⡱⢎⡧⡵
⠀⢃⠐⡠⠊⠄⢃⠄⠀⠀⠀⠀⠀⠀⠀⠀⠎⣸⢫⠗⣎⢧⡳⣭⢏⡷⣹⠞⡧⢽⡌⢷⣓⡼⣯⣕⣳⣜⣣⢞⣻⠼⣖⢯⡞⣧⢷⡽⡆⠀⠰⢌⡳⣒⠦⡤⣌⠵⣳⠛⠷⣯⣷⢿⡿⣯⡶⢿⣜⡷⣍⣶⣧⡾⣥⢿⡼⣟⣽⠘⠙⢛⠙⠛⠛⣖⡱⣯⢿⠿⢀⣠⣴⢾⡿⣽⣿⣦⠀⠀⢤⣾⣿⡷⣶⣦⣤⠠⢿⣿⣯⠿⡿⢾⡄⣛⣶⣾⣟⢿⠦⠉⠖⠯⣳⡝⣎⠷⣮⡱
⠈⡄⢘⠠⢁⠎⡰⠀⠀⠀⠀⠀⠀⠀⠀⠀⡳⡜⢦⡛⣬⠶⢙⣴⡲⢾⡶⣮⠙⡶⣙⠷⣎⠷⣼⡜⣧⢞⣭⣟⣭⢿⡹⣮⣝⣮⡻⢴⡙⠂⠐⠊⠑⠫⠶⣵⠫⣞⡴⣋⢶⣈⠻⣯⢿⣿⣽⣟⣿⢷⣿⣳⡷⣯⢿⡽⣟⡳⢯⢧⠘⢁⣴⣞⣻⡿⢷⣤⣶⣾⣿⢿⣻⣯⡿⠿⣟⣻⠄⠺⢟⡾⣮⢿⣿⣽⣏⡷⣲⣬⡙⣷⣛⠧⠟⠤⢶⡶⠾⡯⡿⠿⣿⣟⣶⣜⠹⡎⣥⠳
⠐⠀⠊⠐⠈⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡹⢶⠹⣆⠋⠈⠸⠉⠙⠀⠃⠀⢳⢹⢎⢹⢻⢆⡟⠖⠛⠲⠏⡞⡏⡟⡶⢏⡖⠿⡉⡷⠃⠀⠈⠳⣉⠓⡸⡙⢲⢱⠻⡖⢻⢳⡘⠻⣱⣿⢹⣾⢻⢷⡏⣿⢃⣿⡞⡷⢱⠏⠃⠀⠾⣉⡟⢁⡶⣿⡟⡾⡟⣷⣿⣏⢱⡟⣿⠞⠋⠀⡀⡶⠓⡎⠹⡆⠉⠊⠉⢈⣁⣈⣀⠒⢻⡟⡷⡆⠉⡙⣿⣹⡟⡏⣾⣾⠟⣇⠘⣈⠓
⠀⡄⠁⡀⢠⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⣷⣌⣷⣡⠀⠀⠁⠀⠀⠀⠀⢀⣧⣹⢸⣉⡞⣼⢀⣶⣿⣶⡆⣤⠁⣧⡇⣦⠘⢂⣁⣁⠃⠀⠀⠂⠀⠓⣡⡜⣹⡌⣧⡘⠊⠂⠉⢢⡈⠙⡟⣤⢻⣦⢻⣼⠛⣼⣇⢣⣏⡞⠀⡘⢂⠉⠉⡈⡗⢹⡄⡑⢋⣹⣠⠘⣾⡙⢀⡞⠁⡑⠀⠑⢀⣀⠒⠀⠀⠀⡞⣼⣿⡟⣿⡟⣿⣀⠓⣿⣆⠙⠃⣠⡙⣱⣠⣉⣶⡉⠐⣀⡎
⠐⣈⣐⣁⣂⣀⣁⣤⣤⣤⣤⣤⣤⣤⣤⣦⣶⣷⣾⣶⡇⠐⠣⠄⠀⣠⠀⠀⢼⣴⣾⡙⢿⣼⡏⠈⠻⠓⠏⠉⠀⠀⢼⡿⢧⣃⣉⣙⣛⣃⡂⠀⠄⠃⠐⠧⠿⠵⡹⠗⣩⣶⣿⢿⣓⣮⣕⢙⠻⣿⡽⣯⣾⣻⡵⢮⣝⡮⣥⣰⠀⢀⠠⠁⠀⡀⢂⣉⣘⠻⢴⣫⢟⡯⣲⠋⠡⡤⠃⠀⠈⠀⢀⠀⠄⡀⠄⠂⢳⣊⢛⡓⠯⣷⡻⠾⣝⣚⣳⢄⠓⢾⠹⠞⠿⢍⠁⡜⡥⢎
⣿⣿⣿⣿⣿⣿⢿⡿⣿⣟⣿⡿⣿⣟⣿⡿⣿⣾⣷⢯⣿⡿⣿⣶⣿⣿⣿⣿⣒⣛⣯⣭⣤⣻⣾⣿⡿⣿⣿⣿⣿⣿⣾⣿⡿⣿⡿⣿⣽⣿⢿⣿⢿⡿⣿⣻⣽⣿⣽⣿⣿⡿⣽⣿⣾⣶⣳⣾⣷⢯⣟⣿⣬⣷⣻⣞⣷⣛⣵⣶⣦⡌⠀⠑⠂⠈⢟⣿⢿⠇⠠⠌⠡⠎⠂⠇⢢⠄⠀⠠⢶⡤⢤⠶⢮⠁⠐⠈⠂⠙⠊⣙⣁⣈⣀⣛⣟⣻⣙⢧⠩⢬⡍⢛⢚⠂⠀⣙⢦⢫
⣳⣽⣞⣯⣷⣿⡿⣿⣽⣿⢾⣿⣳⡿⣾⣿⣽⣾⣻⣯⣿⠿⣟⣿⢾⣷⣿⢾⡿⣽⢯⣯⡿⣽⣷⢯⣿⡷⣯⡿⣷⢯⡿⣞⡿⣯⣿⣽⢾⣯⡿⣿⣯⡿⣽⣷⣻⣷⣟⣷⣾⣻⣿⣛⣾⣽⣷⣻⣾⢯⣟⣷⣟⣞⣯⣟⡷⣿⡽⣿⣽⢿⣯⣽⣭⣶⣶⣶⡶⣶⣶⡶⣤⣤⣤⣨⢤⣤⢄⣈⣌⣛⣁⣘⣩⠄⠈⠑⠂⠰⣿⡻⣟⣿⣿⣯⣿⣟⣿⠧⡀⠠⡌⠐⠁⠀⠘⡜⡎⡞
⣙⡾⣭⢿⣞⣷⣟⣷⢯⣟⣯⡷⣯⣿⢷⣻⣾⣳⢿⣾⣽⣿⣽⢾⣯⣷⣯⡿⣽⣻⡿⣾⣽⡷⣟⣿⣯⣿⡽⣿⡽⣿⡿⣽⡿⣽⢾⡽⣯⣷⢿⡽⣽⣿⣽⡾⣷⣟⣾⡽⣾⢷⣯⣟⣾⣷⣻⡷⣯⡿⣿⣞⡿⣾⡽⣞⣿⡽⣟⣷⣻⣯⢿⡿⣟⣿⢿⣽⣟⣯⢿⣽⢯⡿⣿⢿⡿⣿⢿⡿⢿⣻⡽⣿⠿⣿⣿⡿⣿⡶⢶⡶⣶⣦⢶⠶⣤⢮⣽⣧⢵⣤⣤⣤⣤⣤⣬⣼⣵⣫
⣩⠷⣯⢿⣞⣷⣻⢾⣻⢾⣳⣟⡷⣽⢯⣟⡶⣯⢿⣞⣧⡿⡾⣯⢷⣳⣯⣟⣷⣻⢷⣻⣭⢿⣯⢷⡷⣾⡽⣷⣟⡷⣽⣷⣻⣽⢯⣟⡷⣯⢿⣽⣳⢷⡾⣽⣳⡾⣷⢿⣹⣯⢷⡾⣽⣾⣳⣟⡷⣟⣷⢯⣿⣳⢿⡽⣏⣿⣽⢾⡽⣾⣯⢯⡿⣽⢯⣷⢿⡾⣟⣾⡿⣽⣟⣯⣿⢿⣻⢿⢿⣷⣻⡽⣿⡟⣾⡽⣷⡿⣿⣻⢯⣟⢾⣿⢻⡿⣽⢾⣟⢿⣻⠿⣽⣻⡽⣾⠶⣿
⡸⣟⣧⣿⢮⡷⣯⢿⡽⣯⡽⣾⡽⣯⢿⣞⡽⣽⣻⢮⣽⣳⠿⣝⣯⢷⣽⣺⢧⡿⣏⡷⣯⢿⣞⣯⣟⡾⣽⣳⢯⡽⣗⣯⢷⣻⠾⣽⣻⡽⢾⣳⢯⣯⣽⡞⣷⢯⡷⣯⢷⡯⣿⡽⣷⣳⡽⣮⢿⡽⡾⣽⢾⣹⡿⢾⡽⣶⢯⡿⣽⣞⡷⣻⡽⣽⣳⢯⣷⣻⡽⣾⢽⣳⣟⡾⣼⡷⣻⢯⣟⣶⣻⣽⣳⠿⣽⢻⣷⣻⢷⡯⣟⣾⣻⡼⣟⡾⣽⡾⣽⢯⣿⣻⠷⣯⣽⣫⡿⣽
⢹⣎⡷⣺⣳⣟⣳⡿⣺⡽⢾⣳⢻⡽⣾⡽⢾⣳⢯⡿⣾⡹⣟⣟⡾⣻⣼⣳⢿⣳⢯⣽⣛⣮⡟⣶⢯⣟⣳⢯⣟⣽⡻⣞⣯⢟⣿⣳⡳⣟⡿⣭⢷⣻⠾⣝⣯⠿⣼⢯⢷⣛⣷⢻⣶⣏⡿⣳⢯⣻⡽⣞⡯⣷⡻⢯⣟⡾⣻⡞⣷⢾⣝⡷⣛⡷⣯⣟⢶⢯⢷⣯⣻⢧⣻⡽⣳⡟⣽⣏⡾⣧⡟⣶⢯⣟⣽⡻⣼⢧⣟⢷⣻⡼⣷⡽⣫⢷⡟⣽⡳⣟⡾⣵⣟⡿⣼⣳⣟⣳
⡱⣏⣟⣳⠷⣾⢳⣟⣧⣟⣻⣼⢯⢿⣼⡻⣽⡳⣯⢷⡽⣳⢿⣜⡿⣵⢯⣞⣯⢷⣻⢶⠿⣼⢟⣮⢿⣼⣛⡾⣽⢞⣷⣻⡼⣟⡶⣯⢷⣻⢳⡿⣽⣳⢟⡿⣼⢟⣽⣛⣾⣛⣾⢯⡶⣟⢾⣳⢯⣷⡻⣽⢞⡷⣟⢯⣟⣼⢷⣻⡽⣞⢯⢾⣏⡷⣷⠾⣯⣟⣳⣞⣧⣟⢷⡻⣵⣟⣳⡾⣽⡞⣽⢯⡷⡾⣽⢳⣯⠷⣯⣻⢷⣻⢞⣽⢻⠾⣽⢯⡟⣾⡽⢶⣯⣟⢷⣳⣏⢿
⡰⣛⡹⢞⡿⣝⣻⣼⡶⣯⢷⣻⢾⣻⢶⣟⣷⣻⢷⣯⢾⣟⡾⣏⣾⢷⣻⢾⡽⣞⣿⣺⢯⣽⣾⣹⣞⡷⣯⣟⣷⣻⣮⢷⣻⣽⣳⢯⡷⣯⣟⣾⣳⣟⣾⣻⣞⣿⣺⡽⣶⣟⣾⣳⡽⣯⣟⣧⡿⣶⢿⣹⡾⣽⣾⣻⢾⡽⣞⣳⣟⣾⣫⣟⡾⣽⣳⢿⣳⢯⡷⣾⢧⣯⣟⣻⣳⣞⣻⣼⢷⣯⢯⣳⣟⣳⢯⣷⢯⣻⣗⣻⡾⣽⣻⢮⣿⣫⣟⡾⣽⣳⢟⣳⣟⡾⣽⣳⣞⡿ ''', 0.5)
def tavern():
    echo('''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠞⢿⡕⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⣹⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠖⠁⠀⠀⠀⡟⠻⠓⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣧⣀⣀⣿⣀⣀⣼⡀⠀⣴⠀⠀⢠⠀⠀⠀⢀⣾⢰⣧⠨⢾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠋⠀⠠⢀⡐⠈⣄⡟⠀⠀⠀⠈⢕⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⡿⠁⠉⠉⠉⠉⠙⠙⠛⠻⠳⠶⢿⣶⣶⣷⣼⣿⣼⣿⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡞⠁⠀⡤⢌⣡⠆⡰⠿⠏⠀⠀⠀⠀⠀⠀⢋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡿⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠉⠉⢹⣿⣿⣋⣹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢄⣾⠟⠉⠀⠀⠀⣴⠻⢥⠊⣅⣛⡖⠂⠀⠀⠀⠀⠀⠠⡑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡟⠁⠘⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢧⣿⣟⣉⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣷⠟⠉⠀⠀⠀⠀⠀⣘⠃⠆⠩⠄⣉⠦⡃⠀⠀⠀⠀⠀⠀⠈⠢⡱⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡿⠶⠒⢾⣿⡇⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠘⣿⠨⣿⣏⣩⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠
⠀⠀⠀⠀⠀⠀⠀⢀⣴⢟⡁⠀⠀⠀⠀⠀⡀⠈⠀⠀⠀⠀⢈⡔⢲⡙⠦⡀⠀⠀⠀⠀⠀⠀⠀⠈⠷⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⡿⢷⣶⣶⣾⡟⣿⡤⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠠⠐⣿⡠⣿⣯⣽⣿⣦⣶⣤⣤⣤⣦⣤⣤⣴⣶⣷⣶⣶⣶⣦⣤⣤⣴⣿
⠀⠀⠀⠀⠀⢀⣴⢿⢱⢊⡤⠴⡚⣹⢡⣁⠀⠄⠂⠀⠀⢀⠂⠌⢣⠉⢞⠀⢠⠈⠓⠀⠀⠀⠀⠀⠀⠁⠷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡦⠀⠀⢀⣾⣿⣿⣏⣿⣹⣏⣹⡇⠸⣷⡄⠀⠀⠀⠀⠀⢠⣄⣀⡀⣀⠀⠀⠘⢿⣿⣉⠉⣿⠍⠀⠀⠀⣀⣀⣀⣀⣀⣀⢤⣶⡒⠀⠀⠀⠐⠀⠀
⠀⠀⠀⣠⣴⣿⢛⡢⠃⡌⢲⡙⡜⠦⢫⠀⠀⠀⠀⠀⠠⠀⠎⡘⢄⠣⢰⢠⠞⠀⢰⣧⠀⠀⠀⠀⠀⠀⠈⠠⢳⡦⣠⠂⠀⠀⠀⣤⣦⡀⢀⡀⠀⡀⣀⢀⠀⠀⠀⠀⣀⣶⣖⣾⣿⠗⠁⢠⣾⠟⠁⣸⣯⣹⣹⣯⣹⣇⠄⡈⢿⡄⠀⠀⠀⠀⠘⢏⠘⣏⢛⡟⡟⡿⣞⠛⢧⠞⠛⠀⠀⢀⣼⣟⣉⡏⠉⣏⣉⣉⣹⡇⠀⠀⠀⠀⠀⠀
⠀⢠⣾⣿⡟⣖⡫⢖⡹⢀⣣⡴⢉⣔⡶⠀⠀⠀⠠⠊⠄⡉⠤⡑⡌⠦⣱⠇⠀⠀⠁⠁⠀⠀⠀⠀⢀⠀⡀⠀⠀⢙⣹⢿⣶⣻⣦⣿⡿⡝⣁⢀⣤⣯⣿⣿⣆⣀⣰⣦⣿⡿⠷⡏⠁⢀⣴⡿⠋⢀⡴⣻⣧⣼⣾⣤⣾⡏⢳⣤⡈⢿⣆⠀⠀⠀⠀⠀⠷⣸⠋⢀⣷⢡⣿⡄⢠⣷⣄⠀⢀⣿⣋⣉⣉⣇⣸⣿⣉⣉⡍⣷⠀⠀⠀⠀⠀⠀
⣺⣿⣿⣿⢱⣤⠛⣌⡴⣟⡵⣺⠟⡋⠀⢤⠀⠀⢠⠈⡐⠌⡐⢐⢈⡴⡃⠀⢀⡀⠀⢀⣀⠀⣀⣀⣼⣾⣧⣦⣾⣿⣿⠯⢛⡒⣻⢿⣿⣿⢮⣹⣿⣿⣿⣤⣶⣿⣿⣿⣿⣿⣿⣂⣠⣾⠿⢶⡶⣿⣶⣿⣷⣶⣛⣛⣻⣟⣛⣛⣻⣿⣿⣦⡀⠀⠀⠀⠀⠁⠈⠉⠋⠋⠉⠁⠀⢿⣿⠆⠀⠓⠈⠉⠉⠉⠉⠁⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀
⣽⣿⣿⣿⣯⣀⣽⠿⠛⣤⠟⣱⣮⣽⣔⣯⣸⣆⡶⠊⠒⠠⣐⠢⢏⣾⣉⣶⠸⡁⣸⣾⣿⣶⣯⣿⣿⣿⣿⣿⣿⠛⠂⢂⢦⡑⢥⡠⣙⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠛⠋⣿⣍⠋⠉⣿⠻⣯⠉⢛⣉⠉⡿⣿⣶⣿⣿⣿⣿⣻⢷⣿⣶⠒⠒⢶⣾⣷⣷⢦⣶⣶⣿⢾⣿⡟⠛⣻⣿⠟⠛⣿⡟⣻⠞⢛⣻
⢿⣿⣿⣿⣿⡿⡹⠷⡆⣈⣾⣿⣿⣿⣿⣿⢱⣎⠁⠀⣰⡏⠹⡆⡾⠶⣉⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡉⡁⡏⣆⣹⣶⠿⣷⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠿⡾⡿⢹⣿⣇⣀⣁⣾⣹⣇⣆⡁⣿⣇⢹⣷⣆⣈⣱⣿⠉⣿⠈⢹⡎⠁⠉⢹⠉⡿⠉⠉⣾⢿⣿⡀⠆⠉⢹⣷⣸⣿⣇⣀⣸⣿⣆⣆⣿⣏⣁⣀⣾⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣾⣏⣿⣼⣿⣿⣿⣟⡶⢯⣿⣿⣿⣿⠰⣿⣦⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⣬⣷⣿⣿⣽⣷⡿⠿⣿⣷⣿⣿⣿⣿⣿⢿⣷⣿⡿⠿⢿⡾⠷⢶⡷⣿⡏⢩⡿⢛⣻⣯⣿⣯⣿⣋⣉⠛⣿⣉⠍⣿⠀⢻⠭⢟⠈⢆⠀⢸⠉⡗⢠⠞⠁⢼⡿⢷⣛⠚⢻⣿⣿⣿⣁⣌⣹⣿⣾⣿⣿⣭⣬⣿⣯⠽
⣿⣿⣿⣿⣿⣿⣿⡿⠅⣉⠻⣩⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⡍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⣰⢟⠁⡀⢂⢂⠰⠈⠄⡃⣿⣿⠟⢻⡉⢽⡏⠩⠉⢽⡏⡉⣿⢋⠿⣯⡿⠉⢹⠉⣯⠉⠉⠛⢽⣉⢫⢏⠉⠉⢻⠛⠉⠻⣯⣹⡏⠀⣿⠂⠐⣨⣿⣉⢈⣿⣴⢟⣁⣀⣠
⣿⣿⣿⣿⣿⣿⣧⣐⣀⠋⡡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⢨⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⣋⠀⠢⠁⠆⡀⠢⠁⠆⠄⣟⣿⠶⠾⣿⣿⠖⢳⠛⠛⠛⣿⣿⢛⢛⣿⠛⠉⠉⠉⠉⠉⢹⡏⠉⠉⢿⢻⠛⢛⡿⠷⠿⠟⠾⠟⡓⢛⠛⠛⠟⠛⠻⣉⠋⠿⠉⠉⠙⠉⠉
⢙⣻⣿⣿⣿⣷⣿⣯⡃⢰⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⡿⣿⣿⣼⣿⣿⣯⣄⣀⣶⣀⣹⣿⣷⣤⡀⠀⠀⣀⣀⣀⣠⣤⣤⣤⣤⣴⣯⣥⡴⠦⠷⠶⠾⣾⡿⠷⠿⢿⣿⣿⡈⠁⣿⣿⠌⢶⡿⠶⠿⣿⣿⢌⡘⣿⠀⠀⣤⢤⢴⡀⣾⡅⢠⠤⡼⡜⠀⢠⡇⠀⢘⣥⣴⣢⢥⢰⡟⣿⣿⣎⠀⡟⠛⢻⡿⣄⠀⠀⠀
⠀⠀⠈⠌⠻⣿⣿⣿⣿⡿⢻⣿⣿⡿⠏⠛⣿⣿⡿⡿⣋⣜⣀⢹⣿⣿⣿⣻⣷⠾⡿⣿⣿⣟⣿⣟⣛⣛⣻⣿⣿⣿⣿⣟⣛⢿⣉⣽⢭⣏⠁⡆⣿⡶⣺⠿⠻⣿⣶⣤⣬⣴⣿⣷⡀⠂⢹⡿⣿⠂⠀⣿⣿⡇⢸⣗⠨⡐⣿⣿⠠⣘⣿⠀⠀⠯⠿⠞⠃⣿⡄⢸⠀⣧⡇⠀⢸⣧⡶⣿⣦⣼⣿⣶⣞⠛⠙⠋⠁⢠⣷⣄⣾⣇⡀⠀⠀⢀
⠀⠀⠀⠀⠀⣿⣿⣿⠮⢽⢿⣿⠏⢠⠀⠐⣿⣿⡭⠳⣭⣿⣧⣿⣿⣿⡞⠻⠍⠈⢰⣿⣿⣿⣿⢹⠭⠭⣽⣟⠩⡏⣿⣿⡿⣧⣿⡁⠀⢙⣾⣿⣿⣿⣟⣶⣀⡌⣿⣿⠛⢿⣿⡏⢙⡃⠸⣷⣿⣤⣤⣼⣿⣧⣼⡿⣴⣾⣿⣿⡶⠾⣿⠧⠶⠶⠶⠶⠻⣿⡿⠛⠻⣿⠟⠛⠋⢻⡡⣬⠟⣏⣘⡿⠛⠚⠛⠛⠛⠛⠉⠉⠉⠉⠙⠛⠛⠛
⠀⠀⠀⠀⠀⣿⣿⢿⠆⠈⣶⣿⣆⣀⡴⠦⣽⣿⣹⠀⠀⢸⠀⠹⣿⣿⠀⠀⠀⣦⠈⣿⣿⡧⣿⣼⡁⠀⢹⣿⠀⣿⢿⡧⢻⠋⠊⢹⡽⠋⠹⣧⡟⠳⠾⠿⠟⠛⠺⠁⠀⠒⠟⠟⠛⠛⠛⠛⠛⠉⠀⣾⣿⡟⢛⣃⣀⣀⣼⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⢀⠙⠀⠀⠀⠀⠈⡀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠐⡐⣺⣿⣿⣋⢠⣾⣿⣿⠿⠶⣩⣿⣿⣿⣛⣆⢀⠨⠇⣸⣿⡿⣄⠀⠀⣿⠻⠟⠛⠛⣿⡟⡟⠛⢻⣿⣿⣉⡌⢁⡎⢲⠶⠞⠥⢤⣞⠋⠀⠀⠀⠀⣤⠀⣀⣀⣠⡖⠀⠀⠀⠀⠀⠀⠀⠠⣤⡽⠯⠤⠈⣉⣉⣉⣬⣠⣤⣄⣀⢀⣇⠀⣀⣀⣀⣀⣀⣰⣼⣄⣀⣤⣤⣤⣀⣽⣄⣄⣀⣀⣀⣀⣆⣄⣠⣇⣀⣠⣤⣴⣴⣤⡤⢼
⠀⠀⡈⠅⢉⣙⡈⢟⠫⡍⢿⡁⢦⢐⡵⠿⠻⠞⠏⠡⠍⠟⢳⣯⣟⣿⡿⠶⠜⠿⠒⠛⠛⠛⢻⠛⠟⠛⠛⢻⣧⣤⣈⣹⣏⣩⣉⣛⣛⣻⣿⣓⣒⡚⡛⣛⣏⣉⣭⠥⢾⡇⠀⠀⠀⠀⠀⠀⣀⣀⡠⢤⠄⠀⠀⠀⢀⣀⣉⣀⡘⠓⠚⠛⣿⡟⠋⠙⠉⠉⠉⢹⣿⠋⡏⠉⠉⠉⠉⡟⡏⠈⠁⠀⠋⠛⠿⠟⣻⡿⠿⠿⠭⣽⣟⣛⣯⣽
⠀⠠⠂⠁⠉⠔⡨⠜⢃⠮⢁⢘⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠋⠉⠀⠹⠍⠀⠀⠀⠀⠈⡿⠉⠉⠉⠉⠙⡿⠀⠀⠀⠘⠇⠀⠀⠀⠀⠠⠄⠉⣉⣀⣀⣀⣀⣈⠛⠉⠉⠉⠙⠉⠠⡤⢬⣿⡜⠶⠤⠶⠶⠶⢼⠿⠦⠤⢤⣤⣤⣴⣷⡧⠤⣄⣠⣤⣀⣀⡀⣿⡇⠀⠀⡀⠀⣀⣉⣽⣿
⠀⠀⠀⠀⠈⢀⠁⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⢀⣐⢻⠛⣻⣿⣻⣿⣿⣯⣉⠑⠶⠤⠖⠒⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⠸⠃⠀⠀⠀⠈⠏⣉⠛⠻⡟⠳⠶⠶⠶⣿⣾⡎⠉
⠀⠀⠀⡔⣀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠛⠉⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠐⠂⠀⠀⠙⠛⠉⠉⠀⢀⣀⣉⠟⠛⠛⠉⠉⠉⢰⠶⠶⠶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠚⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢠⢰⣶⣚⣛⣋⣩⣭⣀⡤⠀⠀⠀⣰⠤⠤⠤⠤⠈⠉⠉⠉⠂⠶⠶⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠐⠢⠎⠑⠒⠂⠶⠂⠀⠃⢀⣠⣤⣤⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠋⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠠⢐⠂⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤
⠀⠈⢇⣂⠀⠄⡀⣀⣀⢀⡀⢀⠀⡤⢄⡀⠄⡠⢀⠄⠔⠄⠋⠀⠐⠓⠒⠂⠈⢉⠀⠀⠀⠀⠀⠀⢀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⡀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⣀⢀ ''', 0.5)
def narrator_art():
    echo('''⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⡟⣻⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠻⣿⡿⢿⣯⡹⣿⣿⣿⠟⣿⣿⣿⣿⣟⣃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣧⠻⣿⣯⣿⣷⡘⣿⠇⣼⣿⣿⣿⡟⣱⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣷⠘⣿⣿⣿⣧⣿⣻⣿⣿⣿⠋⣼⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢹⣿⣿⣇⠹⢿⣿⣿⣿⣿⣿⡿⡏⣸⣿⣿⡟⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡎⢿⣿⣿⣆⠈⡇⢹⠻⡾⢽⠋⣸⣿⣿⡟⢱⢿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠿⣷⡼⣿⣿⣿⠀⣷⣸⣏⡆⣸⠀⣿⣿⣿⢧⡟⠿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⢸⣦⠁⠻⢿⡿⣧⠸⣿⣿⣹⡏⣾⡇⣏⡟⠙⣼⡆⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡄⣿⣧⢀⢶⣣⣿⡄⠏⣽⠩⢡⣿⠘⢰⠀⣸⡿⢠⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠟⠻⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣎⢻⣖⠸⣿⠿⣧⢰⠯⠤⢤⡯⣿⠏⢶⠋⠡⡩⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⠟⠻⣷⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠟⠁⠀⠀⠈⢿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⣿⣿⣿⣷⣄⡂⠆⣆⢿⡆⠒⢀⣾⣉⠿⢐⣒⡞⣱⣷⣿⣇⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⡗⠁⠀⠀⠈⠻⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⠁⠀⠀⠀⠀⠀⠀⢻⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⣷⡜⠿⢻⣿⠷⣷⢠⣿⣿⣿⣤⣿⣷⣿⣄⣐⢶⣾⣛⡿⢃⣾⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡿⡟⠀⠀⠀⠀⠀⠀⠈⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⣼⣿⣿⡿⠟⠛⣢⣽⣿⠓⣽⣼⣿⡿⣷⡿⣿⣿⣿⣷⣯⣞⣿⣿⣤⡙⠻⢿⣿⣿⣧⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣆⠀⠀⣀⣠⣤⣶⣶⣶⣤⣾⣛⠉⠛⠻⢷⣼⣿⣿⣿⠀⢠⣾⣿⠿⢱⣿⡿⠋⠻⣿⡏⣷⢹⣿⡿⠛⢿⣿⣎⣻⣿⣿⣄⠀⣿⣿⣿⣥⡾⠟⠛⠉⠛⠷⣄⠀⣀⣀⣄⣀⣀⠀⠀⣰⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣤⣾⠿⠟⠛⠙⠛⢻⠻⢟⡿⣷⣦⣀⠀⡿⣿⣿⡏⣄⣸⣿⠿⢹⣿⣿⡇⢸⣿⣿⡿⠿⣿⣿⣿⡇⢸⣿⣿⣷⢿⣿⣿⣄⢹⣿⣿⣿⡀⠀⠀⠀⢀⣤⣿⣿⠿⠿⠿⠿⣿⣿⣦⡻⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⡁⠀⠀⠀⠀⠀⡾⠀⠀⠙⠻⢙⢻⣾⣹⣷⡿⠉⢉⣿⣿⢓⡟⡟⣿⠃⢸⣿⡟⠧⠀⢾⣽⣿⡇⠚⢿⣿⣿⡛⣿⣿⣿⡌⢻⣿⣿⣷⠀⢠⣴⣿⡟⠋⢶⠀⠀⠀⠀⠀⢉⠻⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡿⢿⣿⡄⠀⠀⠀⡸⠃⠀⠀⠀⠀⠈⢿⣿⣿⣾⡃⠀⣼⣿⣿⣾⣷⡿⢁⣾⠌⣽⣶⠀⠀⠀⣶⡌⠩⣿⡌⢿⣿⣧⠹⣿⣿⣷⣌⣯⣽⡟⣳⣿⡿⠟⠁⠀⠘⢇⠀⠀⠀⢠⣾⣿⠛⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⢿⣿⡠⢀⡠⠐⠁⠀⠀⠀⠀⢀⣄⡂⠙⣷⡙⣿⣶⣿⣿⣿⣻⡽⢁⣾⠋⠀⣿⠿⠀⠀⠠⠿⠇⠀⠘⣿⡜⢿⣿⡀⠙⣿⣿⣿⣿⣧⣼⡿⠻⠃⠀⠀⠀⠀⠈⠓⢄⡀⢦⠹⡿⠀⢿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡐⣾⡷⢦⣤⣤⣤⣴⣶⣿⣟⡷⠄⠈⠻⠯⡿⣿⡿⢃⣾⡇⠜⠀⠀⢰⣶⠆⠀⠀⢸⣷⡀⠀⠀⠈⢳⢸⣿⣿⣦⣈⠛⠿⠿⠿⠛⡀⢀⣴⣶⣦⣤⣤⣤⣴⣾⣷⠈⠂⠁⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⢿⣾⣭⣍⣉⣿⢿⣿⣿⠡⣶⣶⣦⣀⣀⣂⣀⣾⠿⠁⠀⠀⠀⢸⡿⣺⠀⠀⢸⣿⡇⠀⠀⠀⠀⠁⠻⣏⡿⢿⣷⣶⣶⣶⣶⢤⣏⣹⠿⣏⣉⣿⣽⣿⡿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠈⢿⣿⣷⣌⠻⢿⡧⠿⠛⠋⠀⠀⠀⠀⠀⠀⢸⣇⣿⠀⠀⠘⣿⡇⠀⠀⠀⠀⠀⠀⠀⠙⠛⠶⠼⣿⢟⣻⣼⣿⡿⠁⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⡿⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⡟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣌⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠯⣧⣀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⡽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢙⣿⡷⠀⠀⠀⠀⠀⢸⣿⣇⠀⠀⠘⣿⡇⠀⠀⠀⠀⠀⠀⠀⠈⠙⠓⣤⠄⢀⣤⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠤⣤⣀⣀⠀⠀⠐⠂⠀⠀⢘⡙⢠⣤⣤⣤⣤⠠⣤⣽⣉⣀⣠⣤⣍⠁⣀⠀⠀⢀⣠⣤⣠⡤⠛⠋⠫⠤⠼⠿⠿⠿⠶⣶⡤⠄⠀⠀⢀⣠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⣿⡟⠀⠀⠀⠀⠀⠀⣤⣄⡂⠀⣨⣿⣷⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⡧⠙⠛⠋⠹⠿⠛⢛⠋⠈⠿⠯⠭⢏⣛⣛⡻⠿⠿⠿⠿⢿⣿⣿⣿⡀⠀⣀⠀⠀⠐⢿⡁⠀⣀⡀⠀⣀⣠⣤⣤⣤⣶⣦⣤⣄⣀⣀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣇⠀⠀⠀⠀⠀⢰⣿⠟⠛⠛⠛⢻⣿⣿⣿⣿⣭⣿⣿⡿⠟⣿⣈⣿⠷⠄⠁⡀⠀⠀⠀⠹⠆⠀⠀⠀⠀⠀⠉⠍⠛⠻⢿⣷⣶⣾⣿⣿⣿⡿⣿⣿⣿⣟⣋⣼⣋⣹⡟⠁⣴⣿⣿⣿⣿⣿⡿⠿⠟⠟⠛⠤⠄⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡟⢀⣀⠀⠀⣰⠏⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣷⡌⣻⣿⡟⢦⣄⠀⢻⣧⠀⠀⠉⢹⡀⠀⠀⣀⢀⣠⡴⠶⣶⣾⣟⣉⣉⣟⣿⡛⠛⠛⠉⢡⡂⠀⠀⠀⠈⠀⠈⠉⢛⣻⣯⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠀⠼⠇⠀⣴⠇⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣷⣀⠁⠂⢀⣀⢐⡳⡶⢹⣿⠏⠁⣴⣾⣿⣿⣿⣿⣿⠟⠻⢿⣶⣤⣴⣿⠇⠀⠀⠀⠀⠀⠾⢿⣯⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣟⠉⠀⠀⠀⠀⠻⣆⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡙⠐⠃⣿⡟⣼⣿⠇⣿⢯⣼⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠙⣿⣿⣧⣄⠀⠀⠀⠀⠀⠀⠀⠉⢻⣿⣶⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣧⣀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣰⣿⠏⣼⡟⢰⣿⡏⣸⠿⣾⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⢀⣾⣿⣿⣿⠆⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⡆⢠⡄⠀⢀⡟⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢠⣿⡟⢸⡿⢱⣿⣿⢡⣿⡄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣤⣤⣾⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⡇⢸⣷⣀⣶⣿⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢾⣿⠃⠙⠃⢘⣻⠿⣘⠛⢷⣄⡮⡙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⠿⣷⡀⠀⠀⠀⠀⣰⣿⣿⡟⠁⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢹⡇⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⠁⢀⣼⣿⠀⠀⠀⣼⣷⠀⠀⠉⠑⠈⠻⢿⣶⣶⣬⣭⣏⣉⣹⣿⣿⣿⣷⣶⣦⣤⣶⣾⣿⣶⣾⣷⣦⣹⡿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⡿⠆⠉⠉⠉⠙⠭⡉⠛⠛⠿⠿⣿⡿⠿⣿⣿⣿⠻⠋⠉⠀⠀⠀⠀⢸⣿⣿⡄⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀⠒⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠤⠤⣀⣀⣀⣀⡤⠶⠾⠛⠋⠉⠓⠒⠲⠶⠶⠤⠤⠼⠥⠶⠶⠶⠞⠛⠓⠒⠲⠾⠿⠶⣶⣤⣤⣀⣀⣀⣭⣭⣁⠀⠀⢈⣙⡁⠀⠀⠀⠀⠀⠀⠈⢉⣽⣿⣿⣿⣛⡛⠛⠋⠉⠉⠙⠛⢿⣿⣿⣿⣿⣆⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣿⣿⣶⣶⣾⠟⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠈⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⣼⣿⡙⣿⣿⣿⡻⣯⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣧⣸⣿⣿⡇⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣿⡌⣻⣿⡇⣿⣿⣻⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⣿⡇⣿⣿⣳⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠃⣿⢣⣿⣏⣼⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠲⠶⣶⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢇⣾⢡⣾⣟⣾⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⠷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⢏⣼⣁⣿⢯⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢛⡞⣱⡿⣳⣾⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠟⣼⡿⣡⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡏⣾⣿⣴⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣾⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠿⠿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⢿⡷⠶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠠⠭⣓⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ''', 0.5)
def inside_tavernart():
    echo('''⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣩⣭⣵⡆⡙⠻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣁⣶⠟⢛⣛⣟⢰⣿⣧⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⡄⠋⣠⣾⣿⣿⣿⣷⡜⡿⢃⢸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⡼⠁⣼⣿⣿⣿⣿⣿⣿⣿⠰⣿⡆⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢼⠁⣼⣿⣿⣿⡿⢿⣿⣽⣶⣿⣿⡇⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢹⣯⣭⣿⣿⣿⣿⣿⣛⣛⣛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢠⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢋⡥⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣴⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⡿⠃⣿⣶⣿⣭⣽⣭⣟⣻⣛⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⠀⣾⣿⣿⣿⣿⣿⡿⢛⣫⣭⣶⣿⡇⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣋⣐⠐⡇⢸⣿⣿⣿⢿⡿⠿⠿⣿⣿⣿⣿⠟⠻⢰⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠀⣿⣇⠿⣿⣷⣎⢹⣿⣿⡿⢁⣿⢣⡏⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣼⣿⣧⢻⡜⣿⣿⣿⣿⣿⣿⢰⣿⣧⢸⡇⣿⣿⡏⣝⣹⣭⣯⣽⣿⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠀⣿⣏⡛⡿⡿⠛⠈⣭⣴⣾⣟⠃⣸⠃⣿⣿⡿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡄⢇⢻⣿⣿⣿⣿⣿⢸⣿⣿⢸⡏⣿⣿⡇⡇⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⢿⠀⡟⣸⣇⣰⣿⣿⡇⢿⣿⣿⡿⣸⡿⢰⡏⢹⣏⣿
⣿⣿⣿⣿⣟⣛⣛⣛⣻⣿⣿⢸⣿⣿⡇⠸⠿⠿⠿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣋⢻⣿⣿⡏⣛⣛⣛⣿⠿⢿⣿⣿⠿⢿⣿⣿⣿⢸⣿⣿⣧⣈⣉⣛⣛⣋⣿⣿⢸⣿⣿⣸⡇⣿⣿⡁⠀⠿⢿⡿⠿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⣿⠀⣶⣷⢸⣿⣿⣿⣿⡿⡟⢿⡟⣠⡟⣡⣿⣶⣾⣇⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣷⣶⣶⣶⣶⣶⣤⣭⣭⣭⣭⣭⣭⣼⣿⣿⣧⣬⣍⣙⣛⣛⣛⣛⣛⣛⣛⣛⠹⡭⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⡇⣿⣿⣷⣶⣤⣤⣤⣤⣾⣿⠻⠿⠿⢿⣿⠿⠿⠿⠿⠿⠿⣿⣿⡿⠿⢿⣿⣿⣿⣿⠿⠿⠿⣿⣿⣿⣿⡿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⡏⢹⡀⢻⣿⢀⣙⣛⠛⢋⣴⡿⢈⡴⢋⣴⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣛⡟⠛⠿⣿⣿⣿⡿⠿⢿⣿⣿⣿⢏⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣻⣿⢽⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⣛⣛⣛⣻⣛⣛⡛⠓⠀⠂⣿⣿⣿⠸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢠⣶⣿⣿⡇⣹⣯⣭⣭⣭⣝⣻⣿⣿⡟⢿⠿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣃⣸⣷⡊⡉⠺⢿⣿⠇⢸⠋⠴⢋⣵⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣷⣷⣾⣶⣮⣿⣭⣯⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣧⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢰⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣶⣶⣶⣶⣦⣯⣼⣿⣿⣿⣧⣭⣉⣙⣛⣛⣛⣛⣻⣛⣻⠃⣾⣿⣿⣇⠠⠹⠿⠿⣯⣽⣿⣿⣿⣿⡿⢿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⢹⣿⡇⡆⣶⣤⣠⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣻⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢻⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⠋⡆⣿⣷⣷⠼⠾⣿⣥⣤⣬⣿⣭⣽⣿⣿⣿⡿⢛⣿⣿⡛⢛⣛⣛⡛⠛⣿⡿⢿⣿⣿⠿⣿⠿⠿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣧⣼⣿⣿⣿⣧⣤⣤⣤⣤⣼⣯⣭⣩⣭⣍⣿⣿⣿⣿⠀⣋⣸⣿⡇⡇⣿⣿⣿⣿⣿⣧⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣿⣴⣿⣿⣿⣿⣭⣽⣿⣿⣿⣿⣿⣿⣿⣇⣸⣿⣻⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢻⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢨⣯⣭⣟⣛⠛⣿⣿⠛⠛⡷⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⣴⣾⣿⡆⢸⣿⣿⣾⣿⣭⣭⣭⣭⣭⢙⣫⢭⣿⡛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠟⢃⣿⣿⣿⣧⣥⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⣛⢻⣽
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⢛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⡇⣿⣿⣿⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢼⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⣿⣿⣿⣯⢰⣿⣿⡄⢿⣷⣿⣿⣿⢿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣾⣶⢀⣾⣿⣿⡇⣦⣤⣤⣤⣤⣾⣿⣿⣇⣙⣀⣿⣿⣿⡇⢸⣿⣿⣋⣋⣿⣿⠛⠛⠛⢸⣿⣾⣿⡇⣿⣿⣿⣿⣿⣿⣿⣽⡏⣤⣶⣾⣿⣿⣿⣿⣿⡟⣛⣉⠛⠻⠿⠿⣛⣋⣉⣭⣵⣶⣾⣿⣿⣿⣿⢸⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣿⣿⣿⣤⣭⣭⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣽⣿⣃⣿⣿⣿⣘⣛⣻⣿⣻⣛⣻⣿⣿⣛⣟⢿⣿⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢼⣿⣿⡇⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⣿⣿⣿⣿⡟⣿⣿⡄⢾⣿⣿⣿⣿⣾⣶⣶⣶⣶⣾⣷⣯⣭⣽⣽⣿⣸⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⡏⣿⣿⢸⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⡿⠿⠿⢛⣛⢉⣥⢸⣿⠀⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿
⣿⣿⣿⣿⣿⣿⣿⣟⠛⠛⢛⠛⣿⣿⣿⠛⣛⣛⣛⣛⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢹⣿⣿⣧⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣭⣭⣥⣭⣽⣥⣀⣉⣿⣿⣿⣘⣛⣛⣿⠿⢿⣿⣿⣿⣭⣭⣽⠟⣹⣿⣿⡇⠿⠿⡿⠿⠿⠿⠿⢿⣿⣿⣭⣿⡿⣿⣇⣸⣿⣿⣿⣿⣿⣿⣶⣿⣿⢸⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡆⢰⠘⣿⣾⠏⣸⣿⡘⢿⣶⢌⣙⣛⣋⣉⣉⣩⣭⣵⣶⣶⣾⣿⣷⣼⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⣀⣿⣿⣿⣄⣐⣒⣃⣆⣾⣿⣿⣿⣿⣿⣿⣿⣿⣏⣹⣿⣃⣿⣿⣿⡀⢙⣛⣛⣛⣒⣒⣒⣒⠒⡖⠐⠙⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣙⣛⣛⣛⣛⣛⣛⣛⡛⠛⣛⣻⡿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣥⣿⣧⣾⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣵⣿⣷⣄⣰⣶⣿⣿⣿⣆⠁⣿⣿⣿⣿⡉⡻⢿⣾⣿⣿⣿⣷⣌⢻⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣬⣭⣭⣭⣭⣿⣿⣿⣧⣀⣿⣿⣟⣘⣛⣛⣛⣛⠒⠒⠒⠒⣶⢶⠶⠄⢠⣶⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠤⢤⡤⢉⣥⣤⡄⢩⣭⣭⣭⣯⣭⣭⣭⣽⣿⡛⢛⣿⣿⡟⣿⣿⣿⣛⣛⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣿⣿⠇⣿⡇⣿⣦⣽⣿⣿⣿⣿⣿⢸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣷⣶⣾⣭⣤⣤⣤⣭⣬⣭⣥⣴⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣇⣽⣀⣰⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⢰⣶⣦⣾⣿⣿⣿⣿⣿⢿⣿⣿⣿⣷⣼⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠋⣩⣭⠭⠟⠛⠻⢿⣿⣿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡿⣡⡿⣬⣿⣿⡏⢻⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣶⣶⣤⣶⣷⣶⡆⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡶⣿⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⠙⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣛⣛⣛⣛⣛⣛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⢥⡟⣰⣿⣿⣿⡇⢸⢿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡆⣿⣿⣿⣿⣿⢀⣀⣀⣀⡐⠙⣉⣉⣉⡉⣙⠻⣿⣿⣿⣿⣿⣿⣿⣿⠿⠷⠶⠶⠶⢶⣖⡀⣀⣠⣤⣤⣤⣤⣄⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠍⠉⠉⠉⠉⠉⠉⠉⠛⠋⠉⠙⠛⠉⠉⠉⠉⠋⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⢻⢁⣿⣿⢸⣷⣿⠿⠿⣿⠇⢀⣸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡇⣿⣿⣿⣿⣿⢸⣿⣿⠋⢠⣿⣿⢿⣽⣧⡘⣷⡌⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⣴⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣴⣆⣴⣶⣶⡇⣿⣿⣿⡟⢻⣿⠼⠟⡐⣿⣿⠏⣴⣿⣿⡿⢃
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣿⣿⣿⢧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡧⣿⣿⣿⣿⣿⠘⢟⠃⢠⣿⡟⢡⣿⠋⣽⣷⡌⢻⠸⣿⣿⢻⣿⣿⣿⣟⠻⣿⣿⣿⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠿⠿⢛⣃⣨⣵⣾⣿⣷⣿⢧⣼⣿⢿⠟⣰⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡇⣿⣿⣿⣿⣿⢸⠀⠀⣼⠏⣰⡟⡏⠀⢉⡟⠁⠘⠀⣿⣿⠸⣿⣿⣿⣷⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠈⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣥⣶⡇⣿⣿⣿⠟⢛⣥⣿⡿⢡⣾⣿⣿⠇⣘⣛⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣰⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢳⣿⣿⣿⣿⣿⠘⠀⠜⢡⢰⠏⠀⠃⣴⣾⣿⠶⠀⠀⠸⣿⣀⣿⣿⣿⣿⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢹⣿⣿⣿⣿⣿⣿⣿⣿⠉⠙⢻⢿⣿⣿⣿⣿⠏⣰⡸⠟⢉⣤⣭⣽⡏⠎⢜⣋⣭⢀⣿⣿⣿⠏⣼⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⢹⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣰⣿⣿⣤⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢸⣿⣿⣿⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢈⣿⣿⣿⣿⣿⣶⡶⢰⣿⠘⢀⠂⢰⣿⣿⣛⡀⠀⡆⢷⣶⣶⣾⣿⣿⣿⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠘⢸⣿⣿⣿⢃⣾⠏⢀⣾⣿⣿⣿⣿⠏⣾⣿⣿⡏⣼⣿⣿⡿⢰⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣸⣿⣿⣿⣿⣧⢹⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⡎⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⢰⠆⣾⡿⠀⠀⠀⠸⣿⠿⠋⢠⡆⠀⢰⣶⣶⣶⣶⣶⣶⡄⢠⣴⣦⣤⣾⣭⡽⢠⣿⣿⣿⣿⡇⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣸⣿⣿⣿⣿⣿⣿⣿⣿⣄⣀⣀⣸⣿⣿⡏⣬⡏⢠⣾⣿⣿⣿⣿⡟⢰⢻⣿⣿⢸⣿⣿⣿⢇⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡿⠟⢙⠛⣿⣿⣿⣿⡿⢛⣰⢉⣿⣿⣿⣿⠿⠝⢧⣙⠿⣿⣿⣿⣿⣿⡏⣁⣿⣿⣿⣿⣷⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⡿⠿⢈⣴⠋⠀⠀⡀⢀⣸⣿⠇⠀⠘⡗⢀⠸⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⡿⢁⣿⣿⣿⣿⣿⡇⢸⠿⣿⡿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⢡⣿⠀⣶⣶⣶⣶⣶⣿⡇⣿⣿⣿⡿⣸⣿⣿⣿⢸⣿⣿⣿⣿⣿
⣿⡿⠟⢛⣥⣶⣶⣿⣇⢻⣿⡟⣫⣶⣿⣷⣾⣷⣶⣶⣿⣶⣶⣾⣿⣷⣼⢻⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⠟⣡⣶⣿⣦⡈⢷⣧⣤⣓⢨⠈⢿⣥⠀⣀⡁⡄⢰⣬⠻⣿⣿⡟⣭⣤⣭⠝⣿⣿⡿⢃⣾⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡆⣀⠀⠀⠀⢸⡧⢰⣿⣿⣿⣿⣿⣿⠑⠿⣿⣿⠇⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿
⣿⣤⡜⢿⣿⣿⣿⣿⣿⣺⠋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡙⣿⣿⣷⢸⣿⣿⡸⣿⣿⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣰⡏⣾⣿⣿⡿⢿⣿⡌⢣⡙⢏⣻⣷⡈⢻⣷⠸⣿⣧⠘⢿⣷⣌⠻⣷⢸⣿⡿⢰⠿⣿⣧⣾⣿⣿⣿⣿⣿⣿⡇⠈⣿⣿⣿⣿⣿⣿⣿⣏⣠⣿⣾⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢩⣤⣤⣭⣤⣤⣔⢲⢸⣿⣿⡟⢿⣿⣿⡔⣿⣿⣿⡇⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿
⣿⣿⣿⣦⡙⢟⣩⣴⣾⠇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡸⣿⣿⢸⣿⣿⣧⢹⣿⣧⣠⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡟⢰⣿⣿⣿⠃⢸⣿⡇⢸⣿⡼⠻⠉⡿⣆⠁⣂⣜⢿⣷⣌⢿⣿⣷⣌⡛⣿⠁⣼⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣟⢹⣿⢙⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⡇⣸⠘⣿⣧⢰⣿⣿⠿⡇⢿⣿⣿⣷⢹⣿⣿⣷⣼⣿⣿⣿⣿⣿
⣿⣿⡿⢋⣴⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠛⣿⡜⣿⣿⣿⡆⢿⣿⣿⣇⢻⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢡⣿⣿⣿⡁⠀⢸⡿⣡⣿⢸⣿⠟⠿⠗⠈⡄⢻⣿⡌⠛⠟⠄⢻⣿⣿⣷⣮⠈⣛⣛⣛⣻⣛⣻⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⡏⢺⣿⣿⣾⣿⣿⣷⣿⣿⠿⢉⣾⣿⣏⠹⣿⣿⣿⣿⢺⣿⣿⣿⣿⣿⡇⠛⡄⠻⢣⡌⠛⢫⣾⣷⠘⣿⣿⣿⠸⣿⣿⡻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣟⣛⣛⣻⣿⡎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⣄⣿⣧⡈⢿⣿⣿⡘⣿⣿⣿⡌⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣾⣿⣿⡿⣀⣦⢀⣤⣿⡿⣶⣶⣦⣴⡶⢃⣇⢸⣿⡇⣿⣇⠰⠦⠙⢿⣿⣿⣿⣮⣙⠿⠿⠿⠿⠿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⡇⠀⣴⣿⣿⣿⣿⣿⣿⡏⠀⠸⣿⣿⣿⡇⠈⡟⣱⣿⢸⣿⣿⣿⣿⣿⣷⡘⣿⣇⢶⣶⢖⣶⣿⣾⢀⣿⢿⣿⣆⢻⣿⣇⢹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢿⣿⣿⣿⣿⣿⣿⣿⣙⣿⣿⣿⣿⣿⣿⣿⣿⢃⣼⣿⣿⣿⣌⢬⣻⣿⣇⢹⣿⣿⣷⠘⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣾⣿⣿⡟⢱⣿⣿⠈⣿⣿⣿⣙⣿⡿⠿⠃⣸⡏⢸⣿⠰⠿⠋⣴⣷⣶⣦⡙⠿⣿⣿⣿⣷⣄⠻⣟⣸⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠹⣿⣿⡟⠀⢠⣿⠇⣾⣿⣿⣿⣿⣿⣿⢱⡙⠟⣰⣷⣾⣿⣿⡿⠈⣽⡇⠀⢿⡜⣿⣿⡆⢿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡿⣿⣿⣿⣿⣿⣿⠉⣿⣿⣿⣿⣿⣿⠟⠡⠺⠿⠿⣿⣿⣿⣎⢻⣿⣿⡆⢿⣿⣿⣆⢻⣿⡗⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣼⣿⣿⣿⢃⣿⣿⣿⢀⢸⣷⣿⣿⣿⣷⣷⣿⣿⡗⢸⣿⣿⡷⠘⣿⣿⣿⣿⡀⠀⠙⠻⣿⣿⣿⣧⡙⢿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⡇⠀⢻⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠹⣿⠁⢀⣿⡿⣰⣿⣿⠟⡛⢿⣿⣿⡄⣿⣦⡙⠇⣿⣿⣿⡇⢸⣿⠟⢓⣈⠓⠈⢿⠿⣬⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡮⣉⣿⣿⣟⣛⣛⣛⡉⠉⠉⠉⠁⣴⣾⣿⣿⡶⢸⣿⣿⣿⣯⢙⣿⣿⡀⣿⣿⡿⣸⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⢃⣾⣿⣿⣿⢸⠆⣽⢧⣿⡿⢿⣿⣿⣿⣿⠈⣿⡸⣷⠆⣿⣿⣿⣿⣯⣤⣿⣷⣦⡙⢿⣿⣿⣧⡙⢿⣿⣿⡇⣸⣿⣉⣉⣉⣉⣤⣤⣤⣯⣭⣿⣿⣿⣯⣿⣶⣶⣶⣶⣶⣶⣶⣾⢡⣿⡟⣡⠞⣡⣾⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣷⣿⢰⣾⣿⣿⣿⣿⣿⣿⣶⣶⣶⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣯⣭⣭⣥⣭⣥⣧⣤⣤⣤⣤⡀⠻⣿⣿⣿⣅⢸⣿⣿⣿⣿⣶⣻⣿⣷⠸⣿⢀⣿⣿⡇⣿⡟⢰⣾⣛⣿⣝⣛⣩⣯⣒⣀⣘⣀⣲⣶⣦⢸⣿⣿⣿⣿⣿⣿⣿⣿⡯⣼⣿⡿⠃⢺⣿⣿⣿⣿⢨⡘⢫⣼⡿⢇⠸⣿⣿⠙⡋⠠⢟⡡⠔⣀⣙⣛⣛⣋⣭⣬⢻⣿⣿⣿⣦⣝⠿⣿⣿⣆⠻⢿⣧⡼⠿⠿⠿⠿⠿⠿⠿⠿⠿⢿⣿⡿⠿⠛⠛⣛⣛⡛⠛⠃⣶⣶⣶⡾⢋⠜⣡⣾⣿⣿⣿⣿⣿⡇⣿⣛⣿⣿⣿⣿⣯⣷⣼⣟⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿
⡘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠂⣶⣿⣿⣷⡜⢿⣿⣿⣿⣿⢿⣏⠻⣇⠛⣾⣿⣿⣷⡿⢰⡖⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⡆⣿⢸⠛⠛⠛⣿⣿⣿⢱⣿⡿⠁⡆⣿⣿⣿⣿⣿⠸⢁⣾⣿⣿⣿⣶⣾⣾⣶⣶⣶⣿⣷⣿⡟⣿⣿⣿⣿⣿⣿⡀⠛⠿⣿⣿⣿⣷⣮⡛⢿⣿⣶⣦⣭⡐⠠⡀⢀⣠⠄⣠⣴⡿⠟⢋⣁⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠔⣡⣶⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⠹⣿⣿⣿⣿⣿⣶⣿⣿⣾⣽⣭⣭⣭⣭
⣿⣄⡻⢿⣿⣿⣿⡿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣾⣿⣿⣿⣿⣿⣎⢻⡿⢿⣷⠸⣿⣆⢈⡀⢉⠉⣛⡛⣿⣬⣭⣍⣩⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣁⣛⣻⢸⣿⡇⠿⢛⣡⠾⠿⢷⠀⢷⣿⣿⣿⣿⡿⢠⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢻⣿⣿⣿⣿⣿⣇⠀⠰⣿⣿⣿⣿⣿⣿⣦⡙⢿⠉⠉⠉⠉⠒⡈⢡⠧⠶⠶⢾⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⠟⡡⣂⣘⠻⢿⣿⣿⣿⣿⣿⣿⣿⡇⠛⠿⢿⣿⣿⣿⣷⣤⡉⠙⠛⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣷⡦⣙⠻⠿⣠⣿⣿⠏⠁⠤⠤⠸⠿⠿⠿⠿⠿⠿⠿⠿⢿⡿⢀⣿⣿⡿⢿⣿⣿⣿⡄⠹⣆⣿⠖⣩⣭⣼⣷⣿⣦⣤⣤⣭⡅⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢨⣭⣥⢸⣿⡟⣼⣿⣿⣿⣿⣿⣷⣶⣶⣦⣬⣽⣧⣿⣯⣽⣍⣛⣛⡿⡿⠿⠿⣿⣿⡿⢹⣿⣿⣈⣻⣛⣛⣛⣛⣛⣀⣘⣛⣛⣛⣛⣛⣿⣿⣯⣦⣄⣠⣄⢷⣼⣿⣗⣓⣲⣾⣿⣶⣾⣌⢰⣿⡿⠿⠿⠿⡿⢣⠜⠰⠟⢛⣃⣳⡄⣿⣿⣿⣿⣿⡿⢡⣷⣧⣬⣿⣛⣀⣛⣛⣛⠓⢄⣀⡀⢀⠀⠀⠀⠉⠉⠉⠉
⣍⣛⡛⠻⠿⠿⣦⣦⣬⡍⣰⣷⣶⣶⣦⣶⣶⣶⣶⣤⣤⣤⣤⣽⣿⣭⣵⣾⣶⡞⣿⢿⠟⠃⠀⠟⠓⢸⣿⣿⣿⣿⣿⣽⣿⣿⣿⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣽⠘⢛⣛⢸⣿⡇⣭⣵⣶⣶⣶⣶⣭⣝⠛⣛⣭⣴⣾⣿⣿⣷⣾⣭⣭⣭⣛⣒⠲⣶⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡶⣶⣯⣿⣿⣿⣿⣿⡿⡿⣿⣿⣿⣿⣶⡶⠖⠴⣡⡼⠍⠸⠿⠋⣭⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⣮⣭⣭⣭⣍⣰
⣿⣿⣿⣿⣿⣷⣶⣶⣶⡶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣀⣐⣈⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⡟⢸⣿⡇⣉⣍⡿⠿⠿⠟⠟⢿⠿⠿⠿⠟⠉⡛⢿⣿⣿⣿⣿⣿⣏⣉⣉⣉⣏⣿⣧⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣎⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⡏⣤⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠀⣿⣿⣿⣿⣿⣿⣿⣦⣤⣼⣭⣭⣥⣤⣤⣤⡦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠶⢛⣃⢸⣿⡟⣰⣶⣶⣿⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣶⣾⣯⣭⣝⣻⣿⣿⣿⣶⣶⣸⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣷⣶⣶⣶⣶⣾⣿⡟⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠘⣿⣿⣘⣻⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⣛⡛⠛⠻⠿⠿⠿⠿⠿⠿⠿⠋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢹⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢰⣯⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⣛⣛⣛⣿⣿⣿⣿⣿⣟⣋⣉⣉⣉⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⢿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣼⣛⣘⣛⣛⣛⣿⡿⣿⣿⣿⣛⣛⣛⣛⣫⣭⣴⣶⣤⣭⣭⣭⣭⠭⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⢿⣟⣛⣛⣛⣛⣛⣛⣛⣿⣿⣭⣭⣭⣭⣭⣭⣭⣽⣯⣭⣤⣴⣶⣶⣶⣶⣿⣿⣷⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣜⡛⠻⠿⣿⣿⢹⣿⣿⣿⣿⣿⣿⡌⠿⠿⠟⢛⣿⣿⣿⣟⣛⣻⣿⣟⣛⣛⣻⣭⣭⣭⣭⠭⠭⠽⢿⠿⠿⠿⠿⠿⠿⠟⠛⠛⣛⣟⣛⣛⣛⣟⣛⣛⣿⣿⣿⣿⣭⣭⣭⣭⣭⣭⣽⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡿⠿⠟⢓⣒⣀⣚⣛⣻⣟⣛⣉⣉⣉⣉⣉⣩⣭⣯⣭⣭⣭⣭⣥⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢰⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢸⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣽⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡇⡇⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⢻⣛⣟⣋⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣭⣭⣿⣭⣍⣙⣻⣿⣿⡟⠻⠿⢿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡇⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣩⣥⣶⣾⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣶⣤⣭⣟⣛⣛⡻⠿⠿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣧⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣴⣯⣭⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣬⣙⡻
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠘⣿⣿⣿⡿⢿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⣿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠇⠸⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⠀⣙⠳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠛⣛⣛⡛⢩⣭⣴⣶⣶⣶⣶⣾⣿⣿⣿⣷⣦⡙⢿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣦⡑⢦⣭⣝⣛⡛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡘⠀⣿⣷⣶⣭⣝⡛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⡿⠿⢛⣩⣥⣶⣶⣿⣿⣿⣿⣿⣿⡄⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡘⢿⣿⣿⣿⣷⣶⣭⣙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⣝⠻⣿⣿⣿⣿⣿⣶⡆⣿⣭⣙⣛⡛⠻⠿⠿⢿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡿⠟⣋⣥⣶⡄⠹⣿⣿⣿⣿⣽⣽⣿⣿⣿⣿⣿⣮⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡹⣿⣿⣿⣿⣿⣿⣿⣶⣌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣿⣿⣦⣍⣛⠻⠿⣏⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣭⣭⣽⣿⣿⣿⣭⣭⣭⣭⣭⣭⣯⣭⣧⣴⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣠⣶⣿⣿⣿⣿⣿⡄⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⢻⣿⣿⣿⣿⣿⣿⣿⣷⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣾⣿⣿⣿⣿⣿⣿⣶⣶⣧⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣾⣿⣿⣿⣿⣿⣿⣿⣿⡄⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡩⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣎⠿⢿⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡔⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠛⢿⡿⢟⣡⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿''', 0.5)
def witch_art():
    echo('''⠿⠛⠛⠿⠿⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣤⣤⣤⣤⣤⣤⣄⣤⣀⣀⣀⣀⣈⣉⡛⠛⠛⠛⠛⠿⠿⠿⠿⠿⠿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣾⣿⣷⣶⣤⣤⣶⣶⣦⣤⣤⣤⣭⣭⣭⣭⡍⢉⡉⡛⣛⢛⡛⠛⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣿⣿⣯⣯⣭⣭⣭⣽⣟⣉⣙⣛⡻⢏⠟⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢋⣭⣭⣭⣿⣛⣛⣛⣻⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⡻⢿⣿⣾⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣍⡓⣀⣀⣐⣂⣀⣠⣤⣭⣭⠿⢿⣿⣛⣛⣿⣿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢞⣿⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡶⣶⣶⢾⣿⣿⣿⣯⣍⡛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣭⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣾⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣭⣭⠛⣶⢆⣶⣦⣼⣹⣭⣩⡉⣭⣭⣭⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣿⣿⣿⢸⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣇⢸⣭⣿⣯⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣁⣿⢸⣿⣿⣿⣿⣿⣿⣷⣿⣷⣿⣯⠸⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⢸⣿⣿⡾⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣿⢸⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣿⣍⣙⣛⣛⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣝⣿⣿⠿⢿⣿⣿⣿⣿⡿⣟⣿⣿⡿⢟⣾⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡇⢧⢿⡇⣿⣿⣿⢿⠸⡝⡏⣿⣿⣿⣿⣿⣿⢸⣿⣿⣧⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢸⣿⣿⣿⣿⣿⡇⢩⡍⣉⠉⣉⢻⠿⡿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣏⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣍⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣭⣭⣭⣭⣭⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡹⣷⡞⡞⣿⡹⣎⣎⠎⣧⢻⢱⣾⣿⣿⣿⣿⣿⢸⣿⣿⣿⡆⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⡇⣼⠃⣿⢰⡟⢀⣸⡇⣿⢸⢸⢸⢲⡆⢰⡎⣉⡻⣿⣿⣿⣿⣷⣎⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠗⣤⣿⢻⡿⢫⣿⣿⣿⣿⢿⡿⣧⣿⣿⣿⣎⣿⣯⣎⣷⡹⡄⡀⡜⣎⣆⣻⣿⣿⣿⣿⡏⢸⣿⣿⣯⡥⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡓⢸⣿⣿⣿⣿⡿⢇⡇⢸⡇⣾⠇⡟⣿⢸⠋⠏⠛⠋⡾⢀⣾⠃⢾⢇⣽⣿⣿⣿⣿⣿⣿⣮⣝⠻⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⠉⡟⢹⢻⡋⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣛⡟⢵⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⡹⠼⠹⠵⠼⢫⣿⣎⢿⡎⡜⣧⢿⢳⠙⣦⠸⣿⣿⣿⣿⣿⡇⣸⣻⣿⣿⣯⣅⠹⣿⣿⣿⣿⣿⣿⣻⣿⣿⠇⢸⣿⣿⣿⣿⣿⣇⡀⣸⠃⡿⢀⢧⡏⡿⡴⡀⠀⠀⠀⠜⠁⠾⣂⠻⣿⣿⣿⣿⣿⣿⣿⣿⡟⣴⣾⣿⢿⣿⣿⣯⣽⡏⣿⣿⡆⡇⣿⢸⢣⣿⠆⢻⣏⣿⣿⣿⣿⡇⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⡇⣿⣿⣿⣶⣶⣶⣶⣦⣤⣤⣴⠲⣶⣶⣶⣮⣬⣽⣯⣤⣽⣵⣯⣞⣘⣂⡊⢣⠻⣿⣿⣿⣿⢗⣿⣿⣿⣿⣿⣿⡀⢻⣿⣿⣿⣿⣿⣿⣯⣽⡇⢸⣿⣿⣿⣿⣿⣿⠀⣿⠀⠁⢾⢾⠸⢰⠐⢸⠰⡄⢠⠐⡂⣼⠏⣴⣾⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣦⣿⢻⣿⣝⡋⢏⣻⣧⡇⢻⡘⣋⣿⣴⣿⣿⣿⣟⣈⣻⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣯⣿⠛⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣷⣽⣿⣿⢳⣿⣮⣽⣟⣛⣛⣿⠃⠈⣿⣿⣿⣿⣿⣿⣿⣿⡅⢸⣿⢽⣿⣿⣿⣟⡃⡙⠀⢐⣘⠜⠆⠧⠶⠃⡿⢿⠸⣧⠹⠎⢘⣛⢿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠟⣼⣿⣿⠸⠹⠛⡇⡄⠙⢿⣷⡳⠿⠛⠛⣿⢻⠟⣿⣿⣿⣿⠉⡉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⢰⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠛⠛⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⡌⢱⣿⣿⣿⣿⣿⣿⣿⣿⡇⡆⠘⣿⣿⣿⣿⣿⣿⡿⠅⠈⢻⣿⣿⣿⣿⣿⣧⠀⢀⣤⣤⣭⣭⣬⣤⣬⣬⣶⣦⠄⢀⣚⣛⣛⣛⣚⣛⣛⢿⠿⠿⠿⣿⣤⣿⣿⣿⡿⡤⣀⣀⠀⠃⡜⠈⠃⡱⠀⢠⠠⠟⡼⣼⣿⣿⣿⣿⡷⣹⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⢿⣿⣿⣿⣟⣿⡜⢿
⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⢠⣦⣤⣄⠀⠀⠀⠀⠀⠀⣈⣙⠛⣛⣛⠛⠛⠿⠛⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢫⣼⣿⡏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣿⣿⣿⣧⢧⠘⢿⣿⣿⣿⣿⣿⣿⡂⠗⠀⣄⣐⣉⡙⠋⢠⣴⡄⢁⣤⣔⠝⠻⠛⠛⠟⡌⢸⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣴⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣦⣬⣭⣭⣭⡀⡅⢀⣁⣙⣒⡒⠒⠒⠛⢛⡽⢴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠙⣿⣶⣿⣿⣿⣿⣾⣿⣮
⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⢰⣶⣶⣶⣶⡅⣿⣿⢰⣿⣿⡇⢶⣶⣶⢸⣿⣿⠀⣶⣶⣴⡾⢍⢩⣿⣽⣧⣿⣛⣛⣛⣛⣛⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠛⣻⡇⣿⢻⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣹⣿⣿⣿⣾⣻⣿⣿⣿⣿⣿⣿⣿⣿⢏⣿⣿⣿⣿⣿⣷⣶⡲⡸⣿⣿⡿⠟⠋⠠⠰⡷⠀⡿⠓⣱⣶⣈⠙⢀⡰⣛⢛⣥⡥⢷⣶⠀⣁⡀⠻⣿⣿⣿⣿⣿⣿⠟⢠⣾⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢹⢇⣼⣿⣿⣿⣿⣿⡿⣁⣪⣶⣶⣶⣶⣶⣶⣶⣶⢞⣻⣥⣭⣭⣽⣯⣍⣉⣛⣛⣛⣿⣿⣷⣿⠛⠋⠛
⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⠀⣻⣿⣿⣿⡇⣾⣿⠈⣿⣿⡇⣾⣿⣶⢸⣿⣿⠀⠘⢿⣿⣇⢸⡏⣿⣎⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⣾⣦⠰⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣯⣤⣤⣄⣀⡀⢸⣿⡇⡏⢸⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢩⣾⣿⣿⣿⣿⣿⣿⣷⣮⣻⢿⣿⣿⣿⡟⣾⣿⣿⣿⢟⣾⣿⣟⣓⡈⢨⡕⣣⣶⢤⡦⠀⡀⣠⡶⠇⡘⠛⠛⠀⠖⣺⡶⠿⣷⡶⢔⣀⣀⡻⠧⣁⠙⢛⠻⣿⠟⢡⣰⣿⣿⣿⣿⣿⣿⣿⢟⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣣⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣛⣛
⣻⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⠀⢿⣿⣿⣿⡇⣿⣿⠀⣿⣿⡇⣿⣿⣿⢸⣿⣿⠀⣧⠀⠉⡛⠀⣁⠘⣋⢠⡝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⠋⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣿⣿⢻⡇⣿⡏⢸⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⡙⠿⣴⣿⣿⣿⠋⣨⣽⣯⡿⠟⣡⣦⡀⠊⠡⠚⠛⠘⠱⡅⠦⣒⠻⣿⣦⠡⢄⡿⢟⢴⡀⠠⣙⣻⠇⠀⠂⠀⠀⠐⡶⠠⠈⣾⣿⣿⣿⣿⣿⣻⣭⣷⣿⣿⣿⣿⣿⡿⣟⣯⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣟
⣾⣿⣿⣿⣿⣿⣿⣿⣻⠀⢸⣿⣿⣿⠀⣿⣿⣿⣿⡇⣿⣿⢸⣿⣿⡇⣿⣿⣿⢸⣿⣿⠀⣿⣷⡀⠹⠄⢻⣧⡀⠺⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣾⣿⠃⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢿⠗⢿⢡⡘⢣⣿⡇⣾⣿⣿⣿⣿⣿⣿⣿⡫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⣄⠙⡻⢿⣶⣿⡿⠫⠑⢸⣿⠋⠁⣸⡟⠠⠰⢿⠂⠉⠁⠀⠃⠙⣋⠨⠀⡁⠀⡚⠷⠈⠊⠩⢁⠐⣐⠿⢈⠰⠀⣴⣦⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣋⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣏⡆⢸⣿⣿⣿⠀⣿⣿⣿⣿⡇⣿⣿⢸⣿⣿⡇⣿⣿⣷⢸⣿⣿⠀⣿⣿⣿⣄⠀⢸⣿⣧⡀⠿⣿⣿⣷⣝⢿⣿⣿⣿⣿⣿⣿⣿⢃⣾⣿⡧⢠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⡇⢻⡼⣿⣳⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⣭⡄⣼⣿⣿⣮⣑⡉⠛⢉⣴⣾⠜⣫⣾⠇⡀⠌⠑⠦⠀⠈⡑⠮⠀⠉⠨⠈⠒⢠⣀⠄⠰⢆⠐⠎⢀⠰⣶⢋⣶⠉⠦⠀⠬⢛⡃⡹⢿⣿⣿⣿⣿⠿⠏⣩⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⣿⣿⡿⠀⣻⣿⣿⣿⡯⣿⣿⢸⣿⣿⡇⣿⣿⣿⢸⣿⣿⠀⣿⣿⣿⣿⡆⢸⣿⣿⣷⡄⣿⣿⣿⣿⣷⡝⢿⣿⣿⣿⣿⢁⣾⣿⡿⢳⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠃⠀⣼⡇⡸⡇⢹⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣳⣿⠟⢸⣿⡿⣹⣿⣿⣿⢀⣬⡉⠛⣀⡛⡋⠸⣿⡥⠄⠁⠰⠆⠻⣧⡀⠻⠉⠛⠀⠠⠀⠠⠉⢀⠀⠀⠸⠆⠣⠄⠈⠀⠀⡄⠈⠊⠋⣿⣔⠙⠟⠭⣡⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣛⣛⣛⣛⣻⣭⣭⣭⣭⣭⣭⣽⣾⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢩⣤⣭⣿⣁⣀⣘⣻⣿⣿⣃⣻⣟⣘⣿⣿⠃⢻⡿⠿⠨⣿⣿⠀⠿⠿⣿⢿⣿⠀⣭⣽⣿⣷⡝⣿⣿⣯⡿⣿⡆⣿⣿⣿⢃⣾⣿⠏⣰⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⡀⣬⣿⢣⡇⣿⡆⣾⣿⣿⣿⣿⣿⣿⣿⣿⢛⣿⣿⣿⣍⢹⣿⣿⣿⣿⣿⡿⣿⡿⣯⡆⢸⡟⣴⣿⠿⣿⡇⢸⣿⠟⠸⡿⢱⣭⡄⠙⣇⠉⢀⠀⠾⢂⣿⣿⡤⢾⡄⠀⢶⡄⠬⠍⣛⠃⠘⠛⢀⠀⠀⢀⣴⡦⠻⢄⡚⠃⠛⢁⣬⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⣛⣛⣻⣟⣭⣭⣭⣭⣭⣭⣭⣷⣶⣶⣾⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⡎⢸⣿⣿⣿⣷⣸⣿⣿⣷⣦⣤⣭⣭⣥⣬⣭⣭⣬⣭⣭⣽⣗⣼⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠀⠓⢺⣿⢸⡇⢿⣷⡜⢿⣿⣿⣿⣿⣿⣿⢟⣾⡟⠉⣾⣿⣸⠻⢿⣿⡿⣿⡑⣫⣾⣿⠁⢨⣾⣿⣿⢸⣿⢏⢨⣿⣿⡷⣴⣿⠗⠀⢶⠘⣄⣀⠀⠀⣀⢸⣿⣿⣦⡸⠷⠉⠥⠋⣚⣯⣤⣀⣀⠂⠀⣠⣾⣿⡇⠰⠞⠁⠠⠀⠹⣿⣆⣿⣿⣿⣿⣿⣿⣿⠿⠿⣛⣫⣭⣵⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⢹⣿⣿⣿⣇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⣇⣜⢿⣿⣧⣟⢿⣿⣿⣿⡟⠋⡄⣠⣿⣿⣿⣿⣧⠹⣿⣿⡟⣲⣮⡝⣣⡸⡿⠟⢟⠃⠬⠁⠘⠟⠸⠿⠻⢿⣿⡿⡇⠈⣷⣿⠄⠀⠄⠙⠈⠙⣿⣿⣿⣢⠲⢠⣾⣿⣿⣿⣿⣿⣷⣮⡻⣿⣿⠁⠀⣈⡚⠋⣴⡇⠰⢩⠻⣿⣿⣿⢫⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣽⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⢿⣿⣿⣿⡏⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⢿⣾⣻⣿⣷⣯⡻⠏⣴⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⠛⢱⠟⢡⣆⠿⣷⣯⣿⡘⣿⢠⢀⠒⢀⡰⣷⣮⡙⢃⠀⣾⣿⣷⡭⣯⣀⠀⠀⣴⣾⡘⣿⡿⣋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⢦⡻⠆⡈⣀⠉⢤⡌⠠⠀⠜⣥⡽⣿⣿⠸⠿⣛⣛⡉⠽⠿⣛⣩⣽⣿⣿⣿⣟⠹⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠻⠻
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⡏⣉⣉⣉⣉⣉⣉⣙⣛⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⢿⣿⣿⣿⣿⠿⣿⢷⢿⠺⣿⣸⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠋⣿⣿⣿⢾⣿⣿⣟⣿⡿⠟⣠⣿⢿⢿⣜⢿⣿⣿⣿⢟⣹⣿⡆⠍⣸⡿⢯⣾⣿⣿⣿⣿⣮⣤⢠⣤⣀⣓⡱⢹⣿⡄⢾⣯⡿⡟⣾⣉⡿⠊⠰⣿⣿⣿⣦⣿⣿⣿⣿⣿⣿⣿⡻⣿⣿⡿⡛⣿⣷⡆⠈⠰⠆⠠⠀⠀⣨⡀⠘⠀⠀⣸⣥⣴⡆⢶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣴⣾⣶⣤⣶⡆⣶⣦⢀⣄⠀⠈⠉⠉⠉⠉⠉⠁⠀⠈⠈⠛⠛⠛⣿⣿⣿⠏⠛⠉⠉⠀⠈⢰⣆⠀⠀⠰⠄⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⠃⢛⣛⣛⠻⣿⣿⣛⢻⣿⣿⣿⢿⣛⣛⡛⢿⣿⣿⣿⣿⣿⣿⣿⡟⣿⢸⣷⣷⣿⡇⢿⣿⣿⣿⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⡟⢸⣿⣿⣿⠇⢁⣼⠿⢉⣴⣿⣿⣛⠅⠀⢰⣿⣾⢹⣿⣆⢻⣷⣿⡿⠿⣿⣿⣿⣿⣿⡘⡻⣿⣿⢻⣿⣿⣿⣷⣶⣶⣶⣿⣿⣟⠟⢰⣿⣿⣿⣿⣿⣹⣿⣿⣿⠿⣿⢿⣿⣿⣶⡿⠿⣟⠃⣤⠀⢀⣢⡛⣐⢛⡁⠃⣇⡂⢻⣿⣿⣷⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⣿⣿⣿⣿⡇⣿⡇⢸⣿⠀⠀⣾⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⢸⣿⡏⠀⠀⠀⠀⠀⣠⣿⣿⡄⠀⢠⡄⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⠀⣸⣿⣿⡇⠸⣿⣿⣧⢸⣿⣿⠘⣿⣿⣿⠈⢻⣿⣧⢻⣿⣿⢿⣧⢹⣼⣿⠋⠁⠀⢸⣿⣿⣿⠘⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⢸⡇⣘⣯⣶⡗⣾⡗⣁⣀⡿⢛⣀⣀⣙⡛⢛⣛⣋⣤⣶⣝⣿⣿⣿⣇⢛⣿⣿⣿⣿⣿⡟⣸⣿⡸⡗⢏⣛⣿⡝⢿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣿⣿⣿⢻⣿⣻⣷⣿⣿⣿⣿⡿⡿⢣⣶⣶⢰⡇⠽⠀⠌⠻⣛⠃⠹⣟⠖⠸⣿⣯⢻⣯⣛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢹⣿⣿⢸⣿⣇⣿⡇⣾⣿⠀⠀⣿⣿⣿⣿⣿⡏⣀⠀⠀⠀⠀⠀⢨⣿⣧⠀⠀⠀⠀⢠⣿⡿⣻⣿⢀⣿⣿⡀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣧⢿⣼⡆⣿⣿⣿⡇⠀⠹⣿⣿⡄⢻⣿⡄⢻⣿⣿⡆⠘⢿⣿⡄⠻⣿⣷⡙⣿⣿⡟⠀⣄⠀⣿⣿⣿⡿⠠⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣿⣿⣿⢿⣿⣿⣿⣿⡟⢸⣼⣿⣿⡟⣾⣏⣾⠿⣫⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣛⡘⣏⣿⣿⡹⣷⡿⣿⡿⣿⡿⢿⡛⠃⣾⡿⣿⣿⡄⣴⣮⣿⣿⣿⣿⣿⣿⡆⣿⣿⣿⢡⣿⣿⡹⠿⣿⡿⣿⣻⡇⣷⡌⠉⡛⣼⠤⣀⠀⠠⠴⢽⣁⣸⡉⣸⡇⡛⣿⣷⡹⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⢸⣿⣿⣿⡇⣿⣿⠀⠀⠙⠻⣿⡿⠋⢰⣿⣆⣴⠄⢀⣴⣿⣿⣿⣷⣄⡀⠀⠸⡏⢾⣿⡇⠾⣛⡻⠇⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⣿⡇⣿⣿⣿⡇⠀⠀⢹⣿⣧⠘⣿⣧⠈⣿⣿⣿⡀⢹⣿⣷⠀⣻⣿⣿⣌⢻⡟⠂⢻⣆⣿⣿⣿⠇⢀⡄⣸⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⣿⣿⣿⢸⣿⣿⢸⣿⢸⣿⣿⡇⢸⣿⣿⡿⢰⣯⣿⢇⣶⣿⣿⣿⣿⣿⣿⢴⣶⠦⣿⣿⣿⣿⡇⢸⡞⣿⡇⣿⡇⣷⣶⣶⡶⣶⣶⣶⣝⣋⢸⣿⣿⣷⣿⣿⣿⣿⣟⣿⣿⣿⡜⣿⣟⢺⣿⣷⣿⣶⣶⣾⡿⠋⡀⠌⣿⣶⣶⡆⣤⢰⣶⣄⡀⠆⠉⣿⠇⣈⣒⠃⣘⣛⡓⠹⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⢾⣿⣿⣿⡿⣿⡿⠀⠀⠀⠀⢻⠀⠀⢸⣿⢏⣹⡇⣿⣿⣿⣿⣿⣿⣿⠃⠀⢀⣴⣮⠀⠁⠠⢿⣥⣒⣢⠔⢦⣤
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡇⣿⣿⣿⡇⢀⠀⠀⢿⣿⡇⠸⣿⡆⠸⣿⣿⣧⠈⣿⣿⣄⢹⣯⠹⣿⣦⡙⢠⠵⢿⣿⣿⣯⣾⠏⣠⣟⣿⣗⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⢸⣿⣗⢸⡏⢸⣿⢿⡇⣾⣿⣿⠆⠈⠛⠃⠉⠀⣿⣿⣿⣿⣿⣿⣮⡉⣼⢿⣿⣿⣿⣿⣾⡇⡟⢇⣿⡷⣹⣿⣿⣿⣹⣞⠿⢿⣿⣟⣿⣿⣿⣿⣿⣿⣿⡿⣧⡻⣿⣷⠙⠟⣶⣝⣛⠻⢿⣿⠿⢷⣤⣁⣰⣿⡿⠟⠠⠀⡤⠠⢸⢿⡇⣶⣖⣻⣒⣋⢰⠰⣴⣯⣥⣤⡘⢻⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣟⣹⣿⣭⣿⣧⣿⣧⣤⣤⣤⣤⣬⣤⣤⣼⣿⣬⣭⣵⣾⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣷⣿⣷⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢧⢸⣿⣿⡇⢸⣇⠀⠘⣿⣷⡀⣿⣿⡄⢿⣿⣿⡆⠸⣿⣿⡀⢿⣧⣈⣻⣷⠀⣀⠀⣽⡏⢹⠅⣼⣿⣿⣿⠸⣿⠹⣟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣽⣿⣿⢸⣿⡇⢸⡇⢸⣿⢸⡇⣿⣿⡏⡀⢠⢠⣶⣶⠁⣿⣯⣉⠺⣿⠟⣴⢁⣄⢾⣿⢟⣫⣽⣬⡆⢹⡜⣿⡃⣿⣟⠿⢿⢿⢏⢻⣷⣽⢿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⠿⣼⣤⢻⣿⣿⠈⠸⣿⡷⡮⣿⣿⣿⡁⠰⣤⡄⡀⠀⠐⠨⠤⠁⣿⣿⣿⣿⡿⣠⡇⣿⣿⣿⣿⣧⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⠿⠿⠿⢿⣿⣿⡿⢿⠿⠿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⡻⠿⢿⡿⠿⠿⠟⠋
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⢸⣿⣿⡇⢸⣿⠀⠀⢿⣿⣇⠨⣿⣷⠈⣿⣿⣷⠀⢿⣿⣷⠸⣿⢿⣮⣊⢬⡻⣿⡟⣤⣈⣀⠿⣿⣿⣿⣾⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⢸⣿⡇⢸⣧⣼⣿⢸⣷⡏⣿⣿⠃⢠⣿⣿⡿⢰⡭⣻⢋⣤⣩⣾⣇⣾⡞⣮⣽⣎⠛⣛⣽⣇⠀⣷⢸⣧⢿⣿⠀⣶⠾⠸⠌⣿⠟⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣭⡓⢾⣿⣿⡀⢍⣝⣛⡳⠼⠻⠿⢇⠐⠋⢭⠿⣦⠀⠃⢁⠆⣿⢿⣿⣿⡇⣿⣇⢻⣿⣿⣿⡯⠄⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠈⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⡀⣀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⢸⣿⣿⡇⢸⣿⣆⠀⠘⣿⣿⡄⠮⣷⠀⢻⣿⣿⣧⠈⢿⣿⡰⠶⣴⣮⣥⣶⣶⣿⣿⣿⣿⣿⣷⣦⣾⣷⡶⣶⣶⢿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢨⣿⣿⣿⣾⣿⡇⢸⣿⣿⣿⢸⣿⣿⣽⣇⣰⣸⣿⣿⢃⣶⠻⣿⣿⣿⣿⣿⡿⣿⡇⣿⣿⣿⣿⡿⢿⣿⣧⢹⣿⣸⡎⣿⣴⡌⠀⢛⣤⢠⣾⣿⡞⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⡌⡻⣿⣿⣿⣿⣿⣿⣿⣿⡏⠅⣀⠀⠠⠶⠻⠿⢠⣤⠉⣿⢸⣿⣿⡇⣿⣿⢸⣿⣿⣿⣿⡂⠀⠀⠁⠙⠻⠿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠈⠛⠛⠛⠛⠛⢿⣿⣿⣽⣿⢻⡟⠀⢀⣹⣿⣿⣿⣿⣿⣯⣽⣶⣤⣤⠀⠀⠀⠀⠸⠿⣿⣏⣩⣿⣄⣀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⠘⠿⠿⠃⠸⠿⠿⠂⠀⠸⠿⠷⠀⠿⠿⠀⠿⠿⣿⡆⠈⠿⣷⠠⠮⡬⠻⠟⣏⣭⣭⣭⢭⣉⣛⠟⣿⠟⢄⣿⡟⡸⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⢹⣿⠇⣾⣿⣿⡿⣿⣿⣿⡿⠷⠊⣸⡿⣧⣿⣿⡁⣿⣿⣿⣿⣿⣃⣿⡇⢿⣿⣱⣿⡇⢸⣿⣿⡆⢁⣭⣭⠻⠙⢀⣄⣸⠾⣷⡻⠏⢥⡹⡿⢿⣿⣿⣿⣿⣿⣿⠿⣿⣯⢉⣶⠭⢈⠙⢿⣿⣿⣿⣿⣿⣧⠀⡶⠄⠤⠠⢀⠀⠿⢯⠄⣻⡸⣿⣿⡇⣿⡛⢨⣿⣿⣿⣿⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣷⣶⣶⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠉⠺⣿⣿⣿⠒⠘⣿⣿⢛⡟⢻⣿⣿⣿⣿⣿⣇⠀⠀⢀⠀⠀⠀⠈⣿⣿⣿⣿⣏⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡔⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣷⣷⣶⡄⠀⠴⠟⠁⣠⡿⣋⠱⢠⣜⡿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣷⣾⣷⣶⣶⣶⣮⣥⣿⢸⢋⡤⠙⢣⣭⣴⣿⣷⡿⠀⣮⠻⣿⣿⣿⣿⣿⣷⡜⣿⣿⠟⡁⣸⡿⣋⠗⣿⠿⣫⣴⣾⣿⣿⣿⣿⣿⣍⢮⡡⣿⡿⠆⠻⣿⣿⢿⣿⣿⣿⣿⣽⣿⣿⣿⣶⠾⠏⣪⣉⣛⠿⠛⢁⣰⣶⡿⡃⢴⠎⠀⣠⠈⢀⢹⣷⣿⣿⡇⣿⡇⢄⡙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠛⠛⠛⠻⢿⣀⣀⠀⠀⢩⣿⣿⠀⠀⠉⣿⣛⣿⣏⢹⣿⣿⣿⣿⣿⠀⠀⣿⡏⢴⣦⠀⣿⣿⣿⣿⣿⠀
⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⢷⣬⡾⢋⠰⠥⢠⣾⣿⣿⣯⣽⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣥⣨⣤⣶⢿⣿⣿⣿⡟⠁⣾⣿⢃⡻⣯⣿⣿⠈⣹⣧⣿⡏⢸⣇⣿⣇⢿⡈⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢷⠙⠁⢠⣥⣆⢿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣷⣾⣷⣭⡿⣁⡟⡿⢾⡛⣩⣶⣯⢐⣝⢦⠙⢄⣼⣸⣯⣿⣿⡇⣿⡿⣷⣭⡳⢬⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠸⠿⠿⠿⠿⠿⡿⠿⠿⠀⠀⣾⣿⣿⣧⠀⠀⢸⣿⣿⡇⠈⣿⣿⣿⣷⣅⢀⣠⣿⣧⣼⣿⡀⠈⠻⠿⠿⠟⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⡇⠻⢿⢿⠿⠿⠿⠿⢿⠿⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡿⠿⠿⠿⠿⠿⠿⠿⠷⠌⠤⠿⠿⠷⠬⢿⣭⡛⠿⣿⣿⣷⣽⡻⢿⣿⠿⠿⠿⢿⣿⣿⣿⣿⠿⠛⢛⣫⣥⣾⣿⣿⣿⣿⡟⣾⣿⣿⡟⡆⣾⡿⠴⠿⣿⢸⣿⡿⢀⣿⣿⡿⣰⠛⣸⡿⣿⣌⣷⡀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⡞⣣⣌⣛⠯⣬⢻⣿⣿⣿⢛⣷⣷⣿⣽⣷⣿⣿⢉⣥⣥⡽⢛⠛⡁⣈⣐⠧⢼⠟⢀⢀⢮⠻⠀⣿⢻⣿⣷⢻⡇⣿⣿⣿⣷⣭⡳⣭⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠱⠒⠶⠶⠶⠶⠶⠶⠀⠀⠀⠠⣿⣿⣿⣿⠅⠀⠘⣿⣿⠃⠀⠻⡿⠿⡿⠿⠃⠹⠿⠿⠿⠿⠿⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡳⣼⣿⣿⣿⣿⣷⣮⡻⢿⣿⠿⢟⣻⣥⣴⣿⢻⣿⣿⣿⣿⣿⣿⣿⡿⢻⣿⣿⡿⡙⠀⠟⣵⣿⣿⣿⣤⣍⠸⠿⢟⠋⢱⡿⠰⣿⣿⣿⣿⣎⢧⠀⣿⣿⣿⣿⣿⣿⣿⣿⠟⡵⣫⣾⣿⣿⣿⣷⣜⣧⣝⠛⣵⣿⣯⣿⢿⢟⣫⣿⣷⣚⣿⡿⢩⣤⣾⣞⣿⡿⣠⣾⣿⣿⣧⡳⡑⠀⣿⢸⣿⣿⢸⣿⢸⣿⣿⣿⣿⣿⣷⣽⣷⣽⣿⣿⣿⣿⣿⣿⣿⡿⢁⣲⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣦⣸⣿⣿⣿⣿⣿⡟⢻⣭⡍⣿⣭⡝⣿⣿⣮⢻⣿⣷⣿⣿⣯⣟⠳⣾⣿⣿⡿⣛⣉⡙⢸⣿⣿⣿⣿⠿⠿⠯⢠⣿⣿⡏⡴⠃⢀⣾⣿⣿⣿⣿⣛⡛⠐⣰⣿⣷⣶⣾⣷⣝⢷⣿⣿⣿⣮⣧⡛⢿⣛⣛⡛⠿⣟⣫⢞⣼⣿⣿⣿⣿⣿⣿⣿⣿⣎⡓⢘⣛⣛⣧⣜⢻⣿⣣⣿⣿⠛⣋⣼⣛⡘⠋⡅⣿⣿⣿⣿⣿⣿⣿⣿⡦⣿⢸⣿⣿⢸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡅⠈⣭⠉⣽⠍⣿⣿⢻⡟⣿⡟⣿⠛⣿⣿⠛⠛⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣭⣽⣿⣭⣭⣽⣿⣭⣭⣭⣭⣭
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣡⣿⣿⡀⣸⣿⣿⣹⣿⣿⡟⣿⣿⣿⡛⣴⡦⢠⣿⣿⣿⣶⡌⣿⣿⡟⣿⡏⢸⣿⣿⣿⣹⣏⠁⣿⣿⣧⣿⣿⡇⢸⣷⣶⡄⣷⡽⣿⣿⣿⣿⣷⢩⠭⣤⣿⣿⣿⣃⠀⠛⠋⣉⢐⣶⡞⣠⣿⣿⣿⠓⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⣿⡏⣿⣿⣿⣿⣲⣟⣿⣿⣿⣟⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⢼⢣⣿⣿⣿⣿⣿⣿⠖⠉⢰⣾⣿⣿⣿⣿⣿⡷⠄⢻⣿⡿⠻⡿⢿⣛⣛⣻⢻⣿⣿⣿⢸⣿⡜⡛⡻⠿⠿⠿⣿⣿⠿⠿⣿⠉⠉⠙⠛⢿⣿⣷⠀⡏⠀⣿⠀⣿⣿⢸⡇⣿⠃⡟⠀⣿⣿⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣟⠛⠛⠛⠋⠛⠉⠛⠛⠛⠛⠛⠛⠛⠻⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠘⣿⣿⠁⢸⣿⣿⢸⣿⣿⣧⣿⣿⣿⡇⢿⡇⣿⣿⣿⣿⣟⢸⣿⣿⡇⢾⡇⠈⣿⣿⣿⢸⡏⠀⣿⣿⣿⣿⣿⡇⠀⣿⣿⡇⣿⡇⢸⣿⣿⣿⡏⣶⡄⢰⣦⠀⢾⣿⣆⢐⢶⣿⢟⣩⣼⣿⣿⣿⣇⠒⢁⣾⣿⣿⣿⣿⣿⣿⢩⣿⣛⢻⣿⣿⣿⣿⣿⣿⣯⡸⠇⣿⣟⣿⣿⠿⠶⢹⣶⢫⣾⣿⣿⣿⣿⣶⣶⣶⣿⣿⡟⢃⢆⢈⣽⣶⣖⣿⣶⣾⣣⢸⢰⣾⣿⣍⠑⣾⣿⣿⠇⠀⣿⣿⣿⣿⣸⢻⣿⣿⢸⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⡶⠀⠀⠀⢴⣼⣿⣿⢸⣷⢠⣿⡄⣿⣏⢸⣗⣿⠀⡇⠀⠉⣿⡆⢰⣶⣦⠀⠈⠉⠛⠛⠛⠛⠛⠷⠶⠶⠖⠲⠶⠖⠖⠲⠶⠆⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⠀⢸⣿⣿⢸⣿⣿⡏⣿⣿⣿⠇⣿⡇⣿⣿⣿⣿⡏⢸⣿⣿⡇⢽⡇⠀⣿⣿⡗⢸⡇⠀⣿⣿⣿⣿⣿⡇⠀⣿⣿⡇⣿⡇⣾⣿⣿⣿⠁⣿⡇⢸⣿⠀⢸⣿⡟⢸⣄⠸⢿⣽⣿⣿⣿⣿⣧⠀⢸⣿⣿⣿⣿⣿⣿⣿⡄⠁⣡⡆⢻⣿⣿⣿⣿⣿⣿⡿⢠⢻⣿⣾⡰⣷⣿⠟⣴⣿⣿⣿⣿⣿⢿⣻⣍⠃⢁⣾⣇⡎⣾⣼⣿⣿⣿⠻⢿⣿⢱⡎⢸⣿⣿⡏⢸⡞⣿⣿⣗⡂⢩⣭⣻⢿⣿⣿⣝⣿⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠀⠀⠘⢸⣿⣿⢸⣿⣸⣿⣧⣿⡇⣿⣿⣿⠀⡇⠀⠀⣿⣧⢠⣿⡉⠀⠀⠀⠀⠀⠀⠐⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⡶⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⠀⢸⣿⣿⢸⣿⣿⡇⢸⣿⣿⠀⣿⡇⢿⣿⣿⣿⡏⢸⣿⣿⡇⢸⡇⠀⣿⣿⡇⢸⡇⠀⣿⣿⣿⣿⣿⡇⠠⣿⣿⡇⣿⡇⣿⣿⣿⣿⣤⣿⡇⢸⣿⠀⣾⣿⣇⣾⣿⣿⣲⡎⣹⣿⣿⡿⢻⠄⢀⠙⠿⠿⠿⠿⠿⢛⣴⣶⣿⣷⣌⠻⠿⠿⠿⠿⠿⣡⠀⠀⣿⡇⡇⣿⣿⣿⣿⡿⡿⠿⣷⣾⣿⣿⣿⡏⢸⡟⣿⣾⣿⣧⣿⣿⣿⡎⣼⣿⠈⠇⢸⣿⣿⢇⣼⣇⢸⣿⣿⡏⡀⣿⣿⣿⣾⡝⣛⣋⣻⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣸⣼⣿⣿⢸⣿⢹⣿⣾⣿⡇⣿⣿⣿⡆⡇⠀⠀⢸⣿⡈⣾⣏⡀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣷⡹⣿⣿⣿⣿⠀⠀⣿⣿⠀⢹⣿⣿⢸⣿⣿⡇⢹⣿⣿⠀⣿⡇⡹⣿⣿⣿⡿⢸⣿⣿⡇⢸⡇⠀⣿⣿⡇⢸⡇⠀⣿⣿⣿⣿⣿⡇⠀⣿⣿⢧⣿⡇⣿⣿⣿⣿⢸⣿⡇⣸⣿⠀⣿⣿⡇⢹⣯⣿⢃⣱⣿⣿⣿⣇⠋⠰⣸⣷⣶⣦⣭⣍⣙⡻⣿⣿⣿⣿⣿⡿⢛⣁⣤⣴⣾⡿⠀⡟⣿⠇⠛⣮⡮⣛⣻⣾⣿⡜⢻⣿⣿⣿⣿⣷⡇⣃⢧⣿⣿⣏⣿⣿⣿⣇⢸⣵⢰⡆⢸⣿⣿⣾⣿⣿⠋⣿⣿⣷⣿⡹⣿⣿⡿⣠⣿⣿⣇⢧⢿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢀⣿⣿⣿⣿⣾⣷⣾⣿⣿⣿⣷⣿⣿⣿⣿⣷⣶⣶⣾⣿⣶⣾⣿⣿⣿⣷⣶⣶⣾⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣥⣤
⣿⣿⣿⣿⣿⣿⣿⣿⡷⣜⢿⣿⣿⣀⣀⣿⣿⠀⣼⣿⣿⢾⠿⢿⣁⣸⣿⣿⠀⣿⡇⣿⣿⣿⣿⣿⢸⣿⣿⠂⣸⡇⠀⣿⣿⡇⢸⡇⠀⣿⣿⣿⣿⣿⡇⠐⣿⣿⢹⣿⡇⣿⣿⣿⣿⢸⣿⡇⣺⣿⢠⣿⣿⡇⢺⣿⢱⣿⣿⠟⢻⡇⠈⢨⣆⢿⣿⣿⣿⣿⣿⣿⣿⣌⢿⣿⣿⣿⢰⣿⣿⣿⣿⣿⠃⠀⣴⡟⣼⢠⣬⣿⣶⣿⣿⣿⣿⣎⢹⣿⡏⢉⣿⣧⠈⣿⣿⣿⣟⠷⠻⠿⠿⠺⠿⠚⠇⠸⠟⠻⠎⣿⣷⢧⡽⠏⠿⣿⣥⠿⠿⠵⠿⠿⠿⠷⢸⢸⣿⣿⣿⣧⣷⣶⣿⣿⣯⣭⣭⡏⣭⡍⠡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⡆⢻⣿⣿⣿⣿⣿⣿⣿⡿⠟⢸⣿⣿⡿⣿⣿⣿⠀⢻⡃⠈⣿⣿⣿⡇⢸⣿⣿⠀⢻⡇⠀⣿⣿⡇⢸⡇⠀⣿⣿⣿⣿⣿⡇⢀⣿⣿⣸⣿⡇⣿⣿⣿⣿⢸⣿⠃⣿⣇⢸⣿⣿⡇⢸⢿⣷⢰⣶⠸⠟⠀⢠⣿⣿⣷⣝⢿⣿⣿⣿⣿⣿⣿⡘⣿⣿⠃⣾⣿⣿⣿⣿⣏⣾⠀⣭⣶⡹⣎⣿⣮⢿⣿⣿⢿⣿⣿⣞⢿⣧⣿⡿⠡⢘⣭⣽⣷⣶⢟⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣦⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣷⣆⢿⣿⣿⣿⣿⣿⡿⢻⡦⢸⣿⣿⡇⢸⣿⣿⠀⣸⡀⠺⣿⣿⣿⡿⢸⣿⣿⠀⢿⡇⠀⣿⣿⡇⢸⡇⠀⣿⣿⣿⣿⣿⠃⠈⣿⣿⢸⣿⣧⣿⣿⣿⣿⣼⣿⠀⢿⡇⠸⢿⣿⠇⠀⠸⠿⢸⡇⢰⣿⡇⢸⢿⣿⡇⣿⣦⡻⣿⣿⣿⣿⣿⣇⢹⣿⠀⣿⣿⣿⣿⡏⣼⣿⠀⣿⣿⣇⣿⡈⢹⣷⢹⣿⣿⣿⣿⡿⠜⣈⡍⣴⣧⣻⣿⠿⠏⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣻⣿⣛⣪⣉⡿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡾⣿⣿⣿⣿⣿⣾⣿⣿⡿⢛⣩⣴⣿⣷⣮⣛⣿⣥⣼⣿⣯⣤⣽⣥⣤⣭⣭⣭⣥⣼⣯⣿⣶⣾⣷⣤⣿⣿⣷⣾⣷⣶⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣾⣾⣿⣿⣷⢸⣇⢸⣿⣧⠸⡸⣿⣷⣿⣧⢻⣎⢿⣿⣿⣿⣿⢸⣿⠀⣿⣿⣿⡟⣼⣿⣿⠀⢻⣿⣿⠸⣷⠀⣿⣿⢻⣿⠿⣫⣴⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣷⣶⣭⣬⣽⣟⣙⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣭⣵⣶⣿⠿⠿⠿⢛⠿⠿⠿⢿⣷⣮⣭⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⢫⣄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⣯⢸⣿⣿⡇⠁⠏⠰⣿⣿⣧⡝⡜⣿⣿⣿⣿⠈⢿⡀⣿⣿⣿⠡⣿⠟⠙⣦⠈⣿⣿⡄⣿⡀⣿⣿⡆⣴⣾⣿⣿⣿⣿⣿⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣭⣭⣿⣿⣟⣛⣛⣛⠛⠛⠛⠛⣿⡿⢿⡿⣧⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⡟⠛⣛⣻⣿⣿⣿⣟⣟⣛⣛⣛⣛⣛⣛⣛⣛⠛⠛⢫⣼⣿⠟⠫⠵⡞⠛⣛⣛⣿⣭⣿⣿⣶⣭⣛⢿⣿⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⠏⡾⣸⣿⣿⣿⣿⣿⡿⠛⠛⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠛⠛⠋⢸⡇⣿⣿⣿⣧⢹⡇⢠⣤⣽⠟⢉⣿⣝⠛⠛⠁⣠⡸⢿⣮⠉⣭⣧⡘⢿⡷⠸⠇⢸⣿⣧⢻⡇⢹⣿⡇⣿⣿⣿⣿⣿⣿⣿⣧⣛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣡⣿⣿⡟⣡⣾⣿⣿⣿⣿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣷⠻⣿⣭⠈⣿⣿⣿⣿⣿⣿⣿
⣿⢿⣟⣛⣛⣿⣿⣿⣿⣿⣿⣿⡇⣾⢣⣿⣿⣿⣋⠉⠉⠉⠉⠀⣐⣶⣿⣿⣿⣿⣯⣍⠻⣿⣆⢹⣿⠋⢉⣭⣤⠀⢠⣤⣦⢠⣤⣶⡄⠀⠀⠀⠀⠀⢀⠀⢀⣀⣀⣠⣀⣤⣤⣤⣤⣴⣶⣶⣶⣠⣄⣠⣤⣦⡀⣠⡆⢸⡇⣿⡏⣿⣿⡈⠀⠘⠛⠋⠰⢿⣿⣿⡿⠀⢸⣿⣿⢾⣿⡎⢛⡛⠃⣠⣶⡐⠀⠈⣿⣿⠘⣿⠸⣿⣇⢸⣿⣿⣿⣿⡟⠋⢹⣿⣷⡜⣿⣿⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢣⣿⣿⠏⣰⣿⣿⡟⣵⣰⣴⣿⣛⠿⢿⣶⣶⣶⣶⣤⣤⡜⡜⣿⣏⠘⣿⣿⣿⣿⣿⣿
⣿⣿⣶⣯⣝⡻⢿⢻⣿⣿⣿⣿⣷⣭⣸⠏⠙⢛⣿⣿⠿⣿⣷⣦⡀⡈⠉⣿⣿⣿⣿⠟⠳⡮⠻⢸⢻⣇⠘⢿⣿⡇⢸⣿⣿⡌⣿⣿⣿⠆⠡⣶⣶⣌⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⡇⣿⣇⣿⣿⡇⣶⣴⣿⣿⣷⣤⣶⣷⢂⣤⣻⡟⣡⣾⢟⣤⠹⣿⣿⣿⣿⡟⣠⣆⠘⣿⡆⣿⠀⣿⣿⠈⣿⣿⣿⣿⣿⡮⢸⣻⣿⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⡛⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠛⠿⠿⠛⠛⠛⠻⠱⡷⣼⣿⠟⠀⢿⣿⡟⣹⢣⣿⣿⣿⣿⣿⣿⣶⣶⠯⣙⠻⣿⡇⡿⢹⣿⡆⢹⠙⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣶⣍⡻⢿⣿⣿⣿⣁⣤⣶⣾⣿⣿⣦⣤⣽⣿⣿⣿⡇⠀⠹⣿⣿⣷⣶⣿⣤⡘⢸⣿⣄⣈⣿⣷⣀⣿⣿⣷⣁⣿⣿⠀⠀⠸⢿⣿⣆⠛⣿⣏⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡇⣿⣿⣿⡟⣼⢿⣿⣿⣿⣿⣿⣿⢃⢿⡿⣽⢡⢉⢰⢻⡟⣧⢹⣿⣿⣿⣿⢻⣧⣧⢻⣷⢻⡀⣿⣿⡇⣿⣿⣿⣿⣿⣿⣮⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣟⣛⣛⣛⣛⣛⣛⣛⣛⣉⣉⠉⢤⢀⠀⠀⠠⠰⠆⣦⣶⣤⡀⠀⢀⠀⠄⠀⠀⠀⣰⣿⣿⠁⢀⣀⣤⢰⣏⣿⣿⣿⣿⣿⡿⠿⠏⢶⣿⣿⣿⠎⠸⠇⣾⠀⠟⠈⠀⣾⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣟⣛⣿⣿⣶⣭⣻⠿⣿⣿⣿⠿⠉⠉⠉⢭⣿⠛⣿⣿⡇⠀⣿⣿⡿⠈⠟⡟⠉⢼⡿⣿⣿⣿⡿⣿⡟⠛⢻⣿⠿⣿⣿⣷⠄⠀⠀⠙⣿⣷⡘⢿⣾⣦⣙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡇⣿⣿⡟⢹⣿⣿⡿⣿⣿⣿⣿⣿⡌⣾⠃⣿⢸⣸⢸⣇⢻⡀⣼⣿⣿⣿⣿⢸⣿⣧⡎⣿⡸⣧⢘⣉⠀⣿⣿⢿⡿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡿⣿⣶⣤⣌⣰⣾⣿⣿⣟⣥⣦⣔⡆⠀⠀⠀⣾⣿⣿⣿⠿⠀⢽⣦⡼⣯⣛⣛⠿⠟⣵⣾⣿⣟⣋⠿⠿⣣⣆⠳⢸⡟⠀⠀⢠⣦⣹⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣶⣦⣭⡀⣦⣿⣈⣿⡿⠀⠻⣿⢣⠀⠸⣷⣧⠀⠀⡇⠀⣸⡇⢿⣿⠋⠀⢿⣧⠀⠘⣿⣇⢹⣿⣿⠀⠀⠀⠀⠘⢿⣷⣌⠻⣿⣿⣿⣦⣙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣗⣿⣿⢃⣾⣿⣿⡧⣿⣿⣿⣿⣿⣿⡈⢸⡏⢸⣿⠘⣿⠈⣰⣿⣿⣿⣿⡟⣸⣿⣿⢻⢻⣿⢂⡿⠿⠀⠁⠀⠀⠁⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣋⠛⠁⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣮⣯⡌⣛⣛⣛⣛⣿⣿⣿⣛⣁⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⡏⠉⠀⠀⠀⢠⣄⠭⠷⣦⣿⣿⠀⢀⡇⠀⣿⡇⠈⣿⡇⠀⠸⣿⡆⠀⣹⣿⡄⣿⣿⡄⠀⠀⠀⠀⠈⢿⣿⣧⡀⠙⠺⣟⡻⢷⣤⣙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⢸⡇⣼⣿⣿⣿⣧⠹⣿⣿⣿⣿⣿⣿⣦⣄⠸⡟⠀⣴⣾⣿⣿⣿⣿⣿⢣⣿⣿⣿⡾⠈⢛⣀⢰⣶⠂⠀⠀⠀⠀⡀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⢀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣷⣿⣿⣿⣿⣿⢟⣵⡿⢏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢠⡀⠀⠀⠀⠀⢸⣿⠀⢀⣨⣿⣿⠀⢀⡇⢠⢹⡇⠀⢹⣿⡀⠀⢿⣷⠀⠙⣿⣷⠸⣿⣷⡀⠀⠀⠀⠀⠀⢹⣿⣷⣄⠀⠀⠙⠲⣯⣻⣷⣬⡙⠻⣿⣿⣿⣿⣿⣿⣿⣿⠸⢸⣿⣿⣿⣿⣿⣇⢿⣿⣿⣿⣿⣿⣿⣿⠀⣷⡇⢿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣇⠀⢙⣭⣄⠀⠁⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣟⣀⠀⢀⣼⡆⣿⣿⣽⣿⣿⠿⣿⣿⣽⣾⣟⣿⣿⣿⣿⢿⣯⣷⠿⣯⣶⡿⢟⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡇⠀⠠⠇⠀⢺⣿⣿⣿⣿⣿⣿⣶⣾⠷⡆⢸⡇⠀⠈⣿⣇⠀⢸⣿⡇⠘⣿⣿⠄⢿⣿⣧⠀⡄⠀⠀⠀⠀⠻⢿⣿⣦⠀⠀⠀⠀⠙⠳⣯⡻⢶⣤⡙⠿⢿⠹⣿⣿⣿⢢⣿⣿⣿⣿⣿⣿⣿⢈⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⢸⣿⣿⣿⣿⡟⣸⣿⣿⣿⣿⣿⠀⢿⣿⣿⠀⣤⣤⣤⠤⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⠿⣀⣐⣛⣛⣋⣘⢿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣻⣭⣿⣷⣿⣿⣶⠿⣋⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣿⣧⣄⣰⡄⠀⢸⣿⢿⣿⢿⣿⣟⣭⣥⣤⣥⢸⡇⡄⠀⢻⣿⡄⠘⣿⣷⠀⠈⣿⡇⠘⣿⣿⡄⠀⠀⠀⢀⠀⠀⠸⢿⣿⣧⢀⣀⣀⢀⠀⠀⠙⠺⠽⠟⠀⠸⠡⠼⢿⡟⣼⣿⣿⣿⣿⣷⣿⣿⡞⣷⣿⣿⣿⣿⣿⣿⡇⣿⣿⢸⣿⣿⣿⣿⢣⣿⣿⣿⣿⣿⣿⠀⠘⣛⡃⢠⣭⣭⣭⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣫⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣝⢿⣿⣿⣻⣭⣿⣿⣿⣿⣿⠿⣿⣟⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⡟⠉⢩⡁⠀⠘⠿⠈⠁⠙⠋⡛⠿⣿⣿⣿⢨⣷⠀⠀⠈⠻⠃⡀⠘⢛⣂⡀⠚⠋⠀⠙⠛⠡⢼⣿⣿⣿⣿⣿⣦⣀⣉⣡⣬⣭⣭⣭⣭⣤⣤⣴⣶⣾⣷⣶⣶⣶⣾⣷⣿⣿⣿⣿⣧⣿⣿⣿⡇⣿⣿⣿⣮⣿⣿⣿⡇⣿⣿⣸⣿⣿⣿⡏⣸⣿⣿⣿⣿⣿⣿⠀⠀⠿⢀⢸⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣯⣽⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣱⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠍⠉⠚⠉⣠⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠘⣛⣃⣀⣈⣀⣤⣤⣤⣤⣴⣤⣶⣶⣶⣾⣿⣿⢸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⡿⣿⣿⣇⣿⣿⣿⣿⢸⣿⣿⣿⢸⣿⡞⣿⣿⣿⢀⣿⣿⣿⣿⣿⣿⠅⠐⣴⢂⣶⣜⣿⣿⡟⡅⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣷⢸⣿⣿⣿⣿⣿⣿⣶⣯⣭⣽⣫⣭⣭⣭⣟⣿⣟⣛⠻⠻⠿⠿⠯⠿⠿⣟⣡⣍⣛⣛⣉⣀⣀⣀⣀⣀⣀⣀⣠⣼⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠙⠟⠋⠉⠉⠀⠀⠈⠹⢿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⢸⣿⣿⣿⣿⣿⣷⣿⣿⣿⢿⣿⣿⣿⡞⣿⣿⣿⢸⣿⡆⣿⣿⣿⢸⣿⣿⣿⣿⣿⡟⠃⣈⠁⣾⢿⡿⢿⠟⢸⠃⢱⣰⠞⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣀⣀⣶⣦⣴⣶⣶⣿⣿⣿⣿⣿⣿⠿⠿⣿⣿⢸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣧⣿⣿⣿⢸⣿⡇⣿⣿⡿⣼⣿⣿⣿⣿⣿⠿⢀⣿⣶⡄⣶⣶⠆⡴⢀⡀⠺⠋⢯⡅⣿⣿⣿⣿⣿⣿⠿⣛⡛⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢉⣈⣹⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⣓⣾⣾⣜⠿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣸⣿⣿⡈⣿⠁⣿⣿⣧⣛⣛⣛⣛⣛⡋⢀⣾⣿⣿⣧⢻⠏⣼⡿⢸⠁⠘⢻⠻⣠⣿⣿⣿⣿⣯⢠⣤⣀⠻⠿⢛⡛⠷⢶⣮⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠉⠈⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⠿⠛⠛⠟⢿⡇⠀⠀⣨⣍⣩⡙⠿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⠿⠿⠿⠿⠿⠻⠛⡛⣛⣛⣛⣛⣛⣉⣉⣩⣭⣭⣥⣥⣠⣤⢰⣍⣛⡻⠿⠿⣿⣿⣿⡿⠃⢻⣿⣿⣿⣿⣿⣿⡇⣿⠀⣿⣿⡇⣿⣿⣿⣿⣿⠃⣼⣿⣿⣿⢹⣜⢸⣿⠇⣶⣿⣷⣤⣶⣿⣿⣿⣿⣿⣿⣿⣶⠿⣋⣼⡿⡻⣶⢮⣭⣭⣵⢖⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣘⣛⡃⣿⣿⣿⣿⣿⣿⣿⠿⠟⠉⠀⠀⠀⠀⠀⠀⠈⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠘⠛⠻⠛⠉⠀⠀⠀⠘⠋⠂⠀⠉⢙⣛⣉⣁⣈⣙⠛⠻⣿⡟⠉⠀⣀⣀⣀⣠⡀⢠⣤⣤⣤⣤⣴⣶⣶⣿⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠋⣸⣿⣿⣿⣿⣿⣿⣶⢶⠀⠀⠈⣿⣿⣿⣿⣿⣿⣇⢻⠀⣿⣿⢻⣿⣿⣿⣿⡏⢰⣿⣿⣿⣿⢸⣿⢸⣿⢠⣦⡝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣐⣛⣯⣵⣾⣿⣾⡻⢦⣔⡺⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⣶⡿⢛⣋⣭⣥⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣶⣭⢩⣟⣛⣛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⢀⣀⣶⣶⣶⠀⣻⣿⣿⣿⣿⣿⡧⠀⠈⠡⠤⠼⠿⠿⠿⠾⠒⠚⠛⠛⠛⢛⣛⣛⣋⣉⢍⣩⣭⣥⣤⣤⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⡙⣯⡇⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⢸⠀⣿⣿⢸⣿⣿⣿⣿⠇⣾⣿⣿⣿⣿⢘⣿⡌⣿⡔⠂⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣭⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣘⣫⣴⣿⣿⣿⣿⡿⢟⣫⣤⢸⣦⣤⣶⣾⣻⣷⣀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡇⢸⣿⣿⣿⣼⣿⣶⣶⣦⢠⣬⣿⣟⣛⣛⡛⠛⠛⠛⠛⢛⣻⡻⠟⠛⠛⠛⠛⢛⠛⠛⠛⠛⠛⠋⣁⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠂⠀⠀⠀⢉⡉⡭⣍⣉⣄⢹⣿⣿⣿⣿⣿⡏⠀⠀⠀⣴⣶⣶⣶⣔⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⢸⣿⣿⣿⣿⣿⣿⣿⣷⠁⡄⡀⠀⢸⣿⣿⣿⣿⣿⣿⠈⠀⣿⣿⣾⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣼⣿⣧⢻⣧⡀⠁⠀⠀⠀⠈⠉⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣫⣅⣘⢻⡭⣕⡻⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⡒⠀⢀⡤⠤⢹⣿⠃⡼⣿⣿⡏⣿⣿⡿⣿⡟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣾⣷⣦⣦⣴⣶⣴⣿⣶⣶⣶⣶⣶⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⣗⢦⣿⣿⡏⠀⣿⣿⣿⣿⡿⠇⠀⠀⠘⠘⣻⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⣿⣿⡛⢸⣿⣿⣿⣿⣿⣿⢿⠏⣸⣿⣿⣤⡀⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⠄⣿⣿⣿⣿⣿⣿⣿⣿⠘⣿⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢀⢈⡉⢉⡉⠙⠛⡻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢴⡶⢰⣶⡍⣿⠏⣷⣜⡿⠎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠽⠋⢰⣿⡏⢸⡇⣿⣿⡇⣿⣿⢰⣿⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⣦⣴⣶⡾⠁⡈⣹⣿⢉⡚⠻⠿⠟⢛⠉⠭⠀⠀⣴⣶⣿⣿⣿⠿⠇⢿⣿⢿⢿⣿⡛⣿⣿⣿⣿⣿⢻⠸⣭⣭⣿⣿⣿⣷⣾⣷⣶⣿⣿⣷⠰⢳⣹⣿⡟⣼⣿⣿⣿⣿⣿⠇⡜⢠⣿⣿⣿⣿⣧⢹⣿⣿⣿⣿⣿⠀⠀⣿⣿⢻⣿⣿⠿⡛⠇⣿⣿⣿⣿⣿⣿⣿⣿⡇⠻⣿⣿⣿⣿⣶⣶⣤⣤⣤⣤⣤⣔⣯⣮⣭⣥⣴⣷⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⣾⣿⡇⣾⡇⣿⣿⣹⣿⣿⣼⣿⠀⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣾⣿⣧⣧⣧⣿⡿⣸⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⡇⣶⣾⢲⢀⢏⡏⡟⡔⡜⣎⢦⠙⣿⣿⣿⣧⢇⢿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣿⣷⣿⢰⢣⠻⣹⣿⣿⣿⣿⠿⣹⡼⠃⡼⣿⣿⣿⣿⣿⠌⣿⣿⣿⣿⣿⡆⠀⣿⡿⢸⢏⣴⣿⣶⡀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠉⢙⡛⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⢿⣿⣿⣿⣿⣿⣿⠿⣿⠿⠿⠷⠲⢤⣿⣿⢸⣿⢡⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢻⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⡇⠿⠏⠃⢸⡜⠠⠑⠁⠈⠘⠘⢁⣿⣿⡿⠿⠏⠌⠿⠟⣻⣛⣛⣛⣫⣭⣭⣭⣽⣿⣧⡣⢱⣿⣿⢟⣩⣦⡘⢟⠇⢀⠀⣿⣿⣿⣿⣿⡆⣿⣿⣿⣿⣿⡇⠀⠿⠁⣌⣾⣿⣿⣿⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⢰⣿⣿⣿⣷⣶⣶⣶⣦⠤⠬⠭⢭⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣶⣤⣤⣦⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⣿⡿⢸⣿⡿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣦⣄⣀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣾⣿⣿⢿⡿⡿⣇⡀⠀⠀⡈⠇⣨⣤⡄⣤⣴⣶⣾⣿⣷⣿⣾⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣿⡿⣡⣿⣿⡿⠃⠀⣠⠀⠀⢨⣿⣿⣿⢿⣧⢻⣿⣿⣿⣿⠇⠀⡀⢸⣿⣿⣿⣿⢟⣇⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣺⣿⣿⡫⣄⠀⠀⠀⠀⠀⠀⠀⣸⣿⡷⢸⡇⣿⣿⡇⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⡸⡿⢻⣟⣛⣿⢹⡍⢉⡍⣭⠁⢰⢰⣾⣿⡎⠀⠁⢸⣿⣾⡆⢱⠃⣽⣿⣇⢿⣧⢻⣿⣿⣻⣿⢿⣿⣿⣷⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣿⣿⠃⣟⣿⣿⠇⢀⣴⠁⠀⠴⠛⠛⠋⢀⣾⣿⡸⠿⣿⣿⡟⡀⠀⠀⠘⣿⣿⠿⠿⠏⣰⢸⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣟⡯⣈⠀⠀⡄⠢⢄⠆⢠⣿⣿⡇⣿⠁⣿⣿⡇⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣰⢿⠇⣾⣿⢿⣿⣿⡅⣼⠇⣸⣀⠘⡜⣿⢋⡔⡀⡆⣿⣿⣿⠇⣿⢀⡽⣿⣿⢸⣿⢿⣿⣿⣿⣿⣞⣿⢿⣿⣧⣻⣿⡿⠯⠿⠿⠿⠿⠿⣋⣸⣿⣿⣆⠋⠙⠉⣠⣼⠇⠀⠀⠀⠀⠀⠀⣼⣿⠋⠁⠀⠉⠻⠃⠀⠀⠀⣠⣿⣿⣿⣿⣿⡏⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠐⢞⡴⢣⠀⢸⣿⡟⢸⣿⢣⣿⣿⢳⣿⣿⣿⣿⢠⣶⣶⣦⣦⣄⡀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣼⡹⢸⢰⣿⣿⢽⣿⡏⣿⣿⣦⢹⣸⢸⢙⣿⣿⢣⣻⡏⢸⣿⢘⡄⠉⠎⠀⢿⣿⡎⡿⣎⣻⣿⢻⣿⣯⣭⣯⣿⡵⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⡏⠀⠀⠀⠀⠀⠀⠀⠙⠃⠀⠀⠀⣤⣤⣤⡶⢋⣴⣿⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣫⣾⣿⣿⣿⣿⣿⢿⣿⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣺⣿⣾⡆⣾⣿⡇⣾⡿⢸⣿⡟⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣂⣿⠏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢧⣾⣿⠇⠆⠼⠿⠿⢘⣛⣃⣛⣛⣩⣬⣬⣬⣤⣭⣥⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣷⣶⣶⣾⣮⣭⣭⣭⣿⣽⣿⣼⣽⣛⣛⣛⡿⠿⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⡄⣷⢸⡆⢷⡘⣷⢱⣰⡆⣤⡬⣛⠛⣁⠠⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣧⡘⣿⣿⢟⣭⣭⣽⣿⣿⣿⣿⣿⣿⣯⣿⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣿⢹⣿⡇⣸⣿⡇⣿⣿⣿⣿⣤⣿⣿⣿⡿⣟⣫⣭⣶⡶⣹⣿⣧⢸⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡆⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢣⣬⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣮⣭⣽⣟⣛⠻⠿⠏⢣⣹⡜⡇⠻⠈⡇⠹⠂⠟⡧⢿⠆⣻⣆⣛⣻⢻⣿⣿⣿⣿⣿⣿⢇⣛⡋⠉⠛⠛⠛⠋⠿⠿⣿⡿⠇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⢻⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣽⣿⣿⣟⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣸⣿⡇⣼⣿⡇⣿⣿⣧⣿⣿⣿⣿⣻⣿⣭⣶⣾⣿⣿⣿⣿⡇⣿⣿⣿⡈⣿⣿⣿⣿⣸⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣶⣮⣿⣿⣛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣥⣔⣂⢦⣶⣦⣲⣿⣿⣿⣿⣽⡝⣿⣗⢼⣿⣿⣿⣿⣿⠃⣼⣿⣿⣿⣷⣶⣤⣤⣄⣀⠈⠀⠈⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣭⣭⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣯⣭⣭⡝⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⡇⣸⣿⢣⣿⣿⢿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣷⣽⣛⠇⢻⣿⣿⡇⢻⣿⣿⡟⡇⣿⣿⣿⣏⣿⣿⣿⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣝⢿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣷⣮⣭⣛⢯⣻⣾⣻⣿⣷⣽⣿⣿⣿⣿⣿⣿⡏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⢷⣿⡟⣸⣿⣿⢸⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⢿⣋⣴⣾⣿⣿⣿⠸⣿⣿⣷⡇⢹⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣮⣙⠹⣿⣿⡦⣾⣿⣿⣿⡟⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣏⢿⣟⣛⣛⣻⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣵⣿⣿⣿⣿⣾⣿⢣⣿⣿⡏⣾⣿⡿⣿⣿⣿⣿⡳⣿⣿⣿⣿⣿⣋⣵⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣇⢹⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣷⣿⣿⣿⢿⣛⣳⣌⡻⣇⣿⣿⣿⣿⡇⢸⡷⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣛⣿⡿⣿⣿⠿⠿⣿⣿⣇⣸⣿⣿⣿⣿⣿⠿⠿⠿⠿⣹⣿⡟⣸⣿⣿⣇⣿⣿⣇⣿⣿⣿⣿⢻⣷⣶⣯⣯⣉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⡘⣿⣿⣿⡄⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣽⣿⣿⣿⣿⣿⣮⡻⣿⣿⡇⡇⢶⣰⡐⡌⠻⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢢⣿⣿⢣⣿⣿⣿⢹⣿⣿⣿⣿⣿⣿⡿⣘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢸⣿⡏⣇⢿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣫⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⠻⡇⢁⠈⢧⡣⡱⢴⢄⡙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣿⣿⠏⡘⣿⣿⡇⣸⣿⡿⣻⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣭⣯⣼⣿⣷⣹⠸⣿⣿⢿⣿⣿⣿⣿⢻⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢷⣿⣿⡿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠉⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⣿⣁⡔⠁⣬⡢⡹⢮⡢⠙⢯⠢⣀⢌⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⡟⢸⣷⢻⡿⢧⣿⣿⡇⣿⣿⣿⣿⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⡄⠛⣻⣼⣿⣿⣿⣿⣼⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣽⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⡿⠿⠋⢉⣠⣴⣥⢿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣽⣿⡆⣿⢘⢿⡝⣏⣦⠻⣮⠢⡝⢮⠳⡝⢦⢢⡈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⠃⣼⣿⡎⣽⣾⣿⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⠿⠀⠀⠁⢿⣿⣿⣿⣷⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣟⣩⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠭⢀⣤⣶⣿⣿⣿⣿⠘⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢹⡼⣯⠿⣎⢧⠣⡹⣷⡍⢮⠳⣜⢶⡱⣝⢎⠢⡀⢀⠉⠉⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣾⣿⡟⠰⣿⣿⣷⢹⣿⣿⣿⣿⣿⣿⣿⡇⠾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⢰⠀⡀⣶⣿⣿⣿⣿⢻⠀⣿⣿⣿⣿⣻⣿⣿⣾⣿
⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣛⡿⠭⠖⠋⣴⣾⣿⣿⣿⣿⣿⡿⠟⢁⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⠿⣻⣽⣿⡿⢸⡇⠹⣷⣻⣎⢧⠳⠹⣿⣧⡱⣌⢦⡹⢎⠳⠑⢌⣢⣕⣄⣀⢄⡀⠉⠹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⣿⢠⣧⢻⣿⣿⢼⣿⣿⣿⣿⣿⣿⣿⠁⠛⠀⠻⣿⡿⠟⠋⠉⠉⠉⠉⠉⠉⠛⠛⠘⠛⠛⠻⠿⠿⠿⢾⡆⣿⣿⣿⣿⣷⣹⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢟⣻⡭⠔⠚⠉⠉⠀⠀⠀⠀⣠⣿⣿⣿⣿⠿⢛⣥⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⢿⣵⣿⣿⣿⡿⣱⣿⡇⠹⠎⢳⡙⣬⡁⣡⣿⣿⣿⣦⣤⠿⣾⣷⣝⢎⠻⣿⣷⣟⣷⣝⣮⣦⡰⢄⣍⢉⠛⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⢃⣿⣿⡸⣿⣿⢸⡇⣿⡙⣿⣿⣿⣿⠀⠀⠀⠀⢸⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡘⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⠿⠿⠟⢛⣛⣛⣭⠭⠒⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⡿⠿⣛⣭⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⢟⣼⣿⣿⡇⢈⣛⢷⣟⣿⣿⣎⢻⣿⣿⣿⣿⣿⣈⡻⣿⣷⣽⣷⣽⢳⣟⢾⡝⣿⣿⣶⡙⢿⡛⡻⣶⣄⢄⣀⡈⣉⠛⠛⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣿⣿⠏⣾⣿⣿⣧⢹⣏⣼⣿⡏⣿⣿⣿⣿⡏⠀⠀⠀⠀⠘⠛⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⠸⣿⣮⣻⣿⣿⣿⣿⣿⣿
⠶⠖⠚⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣚⣩⣭⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⣿⣿⣿⣿⣇⢠⣿⡻⣮⡳⣟⢯⡳⣮⠻⣿⣿⣿⣿⣮⡪⠻⣷⣝⢯⣳⣝⠧⣟⢾⣟⢮⡻⣦⣙⢮⡪⣛⣿⢯⠻⣾⣷⣝⢶⣶⣦⡄⡠⣄⡉⠛⠛⠿⠿⠟⠛⠙⠉⠘⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣾⣿⡏⣸⣽⣿⣿⡟⠈⢿⣿⣿⣷⣻⣟⣿⣿⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤⣤⣤⣤⣤⣤⣻⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⢟⣼⣿⣿⣿⣿⣿⣿⡀⣿⣿⣮⣻⣮⡻⣾⢦⡳⡀⣙⣿⣿⣿⣿⣮⡊⣛⢷⣌⢫⡳⣝⢿⣟⢷⡻⣾⢿⡢⡹⣮⠪⡳⣜⢮⡻⡳⡓⢝⢿⣿⣿⣿⡟⣿⣿⣷⣤⣀⢀⢄⡀⣤⣤⣤⣤⣀⢀⣀⡀⣀⣀⣀⢀⣿⡟⣰⣿⣿⣿⡿⠁⠀⣸⣿⡿⢈⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣤⣤⣤⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣡⣾⣿⣿⣿⣿⣿⣿⣿⡇⣯⡻⣿⣇⠹⣿⣾⣳⣝⢮⢪⡢⡻⡳⡽⣿⣆⠪⡳⣝⢷⣌⢮⡳⣎⢷⡹⣦⣳⡝⣜⣜⢷⢈⡪⡓⣌⢮⡳⣔⢕⢝⠻⣿⣿⣆⡛⣷⣿⣿⡳⣑⣝⢮⡻⡻⣿⣿⣿⣿⣿⣿⣿⣿⣗⡛⠐⠿⠛⠉⠙⢁⢀⢠⣿⣿⣇⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣾⣟⣾⣿⣧⡮⣿⣷⠻⣮⢳⡹⡽⡼⢜⢞⢿⣷⣞⢮⡣⡛⣷⣟⣾⢳⣝⢪⣙⢽⣾⣮⣺⡻⣕⢜⢮⡳⡝⢌⠣⡡⠑⢝⢿⠿⠶⠸⣋⣛⡛⡈⣂⢠⢠⣴⣄⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢣⣿⣿⢸⣿⣿⣿⣿⣿⣿⡟⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣫⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⡯⠻⣿⣿⣼⣿⣷⢻⣯⢻⡼⣜⢮⡫⡳⡿⣿⣷⡿⣝⢮⡻⣷⡷⣝⢷⡻⢮⡻⢝⠿⠿⠜⠻⠆⣙⣙⣦⣇⡔⣤⣤⢢⣸⣧⣳⣿⣿⣿⣾⣪⣋⢻⣻⣿⣷⣿⣮⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⡇⣾⣟⣿⣿⣿⣿⣿⡇⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⡿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢟⣫⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢸⣷⣿⣞⣎⣿⣿⣿⣿⣥⢹⣷⡽⣮⣻⣑⣜⠮⡨⡩⡿⢎⣳⣝⣎⣿⣈⢥⣼⣶⣷⣶⣶⣶⣮⣾⣸⣽⣿⣷⣯⣷⣿⣝⣷⣳⣽⣷⣽⣿⣿⣽⢽⣮⣻⣵⣥⣻⣽⣯⣿⣷⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣽⣿⣿⣿⣿⣿⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⢿⣿⣿⣿''', 0.5)
def witch_hut_art():
    echo('''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠓⠕⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠊⣰⣿⣄⠰⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⢁⣴⣿⣿⣿⣧⠈⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠝⣰⣿⣿⣿⣿⣿⣿⣿⣆⠒⠦⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠏⢠⣿⣿⣿⣿⡻⣾⣿⣿⣿⣆⠐⡛⣇⠠⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⢣⣿⣿⣿⢿⣿⣦⡿⡇⣏⡿⣿⣆⠐⡹⣿⡞⠶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⠀⣾⣿⣿⣿⠸⢹⠲⢳⠃⣻⡟⢻⣿⡆⠘⢻⢮⡆⠠⡡⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠳⢰⣿⣿⣿⣶⡿⣖⣩⣩⣙⡳⣴⣾⣿⣿⡄⠈⢧⡻⣾⢿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣘⠆⣼⣿⣿⣹⣞⣼⣿⡟⡿⡿⣿⣮⣿⣿⣾⣷⠐⣼⢿⣄⢺⣕⣿⣥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⢠⣿⣿⣿⣿⣿⡟⡃⣀⡇⠇⡅⠉⠿⣿⣿⣿⣆⠈⠳⣝⢿⡿⠛⣟⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣾⠏⢀⣴⣿⣿⣿⢻⠻⣿⠀⢀⣿⡶⣿⣶⣦⡅⠙⣷⠉⢿⣷⣄⠘⢷⣱⢆⣼⣾⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡾⠋⢀⣴⣿⣿⢿⣷⠁⢆⠀⢸⠐⣾⡟⡷⢧⠿⡷⣷⠀⢇⠀⠸⠹⣿⣷⣄⠈⢀⡍⢧⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⣿⣿⣿⡟⡈⠙⣴⠸⠀⠀⡀⡏⠔⢂⠖⠆⠖⠂⠀⠀⠀⠏⡜⠋⢻⣿⣷⣼⣿⡿⠿⢏⠋⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⡄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢛⡑⣠⢀⠸⡇⡆⠀⠃⢱⡆⠄⢒⢀⡀⠼⠤⠤⣤⣴⣀⡓⣵⣿⣿⣿⣿⣿⣶⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀⣠⢰⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣃⣵⠩⢢⢄⠀⠀⠀⠀⠀⠀⠀⣀⠤⠤⡴⢡⣿⡄⠖⡛⠓⠒⠒⠒⠒⠾⠞⠻⠟⠒⠒⢓⣂⣀⣒⠒⣶⣶⣶⣶⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⣠⡴⠿⢹⣦⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⡽⢳⣤⣨⠒⠺⣧⣤⣀⣀⣀⡀⠈⠉⢹⢃⣿⣿⣿⡈⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣭⣭⣉⣀⣤⣤⣶⣶⣦⣬⣀⣆⡠⣤⡶⢛⣸⣧⠞⣯⢧⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠐⢲⡿⢷⡆⠐⢋⠛⠟⣦⣽⣴⣡⣇⣿⣽⡿⠱⣻⣿⣿⢻⣿⠒⢸⡟⠛⠙⣿⣿⠿⠿⠛⠉⠛⠿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣱⣧⣿⡷⠟⡹⣄⣰⡿⣺⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠏⠀⠀
⠀⠀⠀⠀⠀⣷⣮⠛⠿⣾⡶⣇⣽⠶⠿⠟⢛⣛⣛⠷⢱⣿⣿⣿⢸⣿⣧⠸⢿⣆⠀⡁⢇⣖⢸⠐⡆⠁⡘⡉⠆⠉⡙⠿⠿⠿⠿⠿⠿⠿⠿⠧⠼⢤⣞⣼⣶⢿⡻⣿⢕⣵⣿⡟⠀⠀⠀⠀⢀⣄⢈⣴⣟⠁⠀⠀⠀
⠀⣤⡄⣠⣤⡿⠛⢺⣴⣸⣣⣻⣿⣿⣿⣿⣿⣿⠃⢣⣿⣻⣿⣿⣸⣿⣿⣧⠀⡹⣷⣆⠘⣛⢛⠛⡗⠀⡄⠐⠒⢺⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣶⣿⡽⡟⣋⣿⣿⣿⠃⠀⢀⣤⡶⢟⡋⠿⢻⠟⠁⠀⠀⠀
⠀⢸⣦⠴⣬⣳⠶⣦⣤⣏⣍⣶⣶⣶⣶⣶⣶⠦⢡⣿⣿⣿⣾⣿⣿⣿⣿⣿⣷⡐⠾⡟⠿⢮⣬⣠⡴⠞⢘⣠⢊⢵⡆⡑⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣷⣾⣾⣿⣿⣿⣿⣴⣾⠿⢏⣈⠤⣤⡶⢟⠳⠒⠒⡢⠄
⠀⠀⠈⠙⠛⣛⡿⣿⣿⣷⣿⣿⣿⣿⣿⡿⠣⢠⣾⣿⣿⣇⣽⠟⠛⠛⠻⣿⣿⣷⡄⢐⣄⠀⢸⠀⠀⠀⠸⣇⢼⡇⣗⣗⠀⡾⢙⢻⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⠿⣿⣿⣷⠴⣞⠺⢿⡿⠞⡀⠀⠀⠀⠀⠀
⠀⠀⣰⠵⠾⠁⠚⣿⡇⣇⣿⣿⣿⣿⣿⡅⢡⣿⣿⡿⠋⣡⣵⣶⣶⣶⣾⣶⣭⡻⣿⣄⠩⣇⠚⡆⠑⠂⠐⢻⣆⡣⠳⠑⣠⠃⡆⠉⣻⣿⣿⣿⡿⠋⠉⢿⡇⢏⣿⣿⣿⠿⣾⢏⡅⠀⠀⠉⠀⣈⣦⠀⠒⠂⠉⠂⠺
⣘⠿⣿⣿⣿⣿⣿⣿⣧⣀⠀⠀⢀⡏⠀⣰⣿⣿⣟⢵⣾⠿⣿⣿⣿⣿⣿⣿⣏⣿⠿⣿⣷⡀⢵⣧⢤⣐⣈⡠⣛⣹⣷⣾⠥⠴⠛⢛⣋⣉⣁⣀⣤⣴⣶⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠛⠓⠒⢢⢂⠁⠀⠀⠀
⠉⢉⣭⣭⣭⣶⣶⣶⣿⣶⣶⣿⢉⢀⣼⡟⢾⣿⣹⣾⣿⣿⣿⣿⣿⠛⣻⣃⣘⣻⣾⣧⡿⣿⣄⠉⠧⣴⣶⣼⣶⣦⣶⡦⣤⣶⣶⡴⣾⣿⡿⣿⣿⣿⡏⣿⣶⣦⣶⣧⣬⣭⣭⣹⣯⣿⢶⠼⠒⠒⠀⠉⠀⠠⠄⢀⠀
⠀⠘⠓⡏⡿⢿⣿⣿⢹⡗⢯⠐⣱⣿⣿⡙⣌⠜⡟⣻⣿⣿⣿⣿⣟⣾⣿⣿⣿⣿⣛⣿⢭⣿⢛⣷⡄⠈⣽⣿⣿⣿⣿⡇⣿⣿⣿⠀⣿⣿⡇⢹⣿⣿⠂⣿⣿⡷⢸⣿⣿⣿⡟⣿⣿⣿⣥⣤⣤⠒⠦⠤⠐⠂⠀⠉⠀
⠀⠀⠀⢹⣀⣠⣿⣿⠸⣇⣼⣿⢹⣿⣿⣷⣌⣦⣹⣿⣿⣿⢋⢸⣿⡿⣿⣿⣿⣿⣿⡟⡌⣇⣼⣿⣿⣿⣿⣿⣻⣿⣿⡇⣿⣿⣿⠀⣿⣿⢷⢸⣿⣿⣾⣿⣿⡇⢸⣿⣿⣿⠁⡇⣿⣯⠻⣿⠀⠁⠀⠀⠀⡀⠀⠀⠀
⠀⠀⣠⡼⣿⣿⣿⣿⠎⣿⢹⣿⢼⣿⣿⡿⢛⣿⡇⣿⣿⣿⡏⡉⡿⣿⣿⣿⣿⣿⣿⣷⡧⢿⣿⣿⣿⣿⡿⣿⣴⣷⣭⡇⣿⣿⣿⠧⢻⣿⡇⣿⣿⣿⢸⣿⣿⡇⣺⣿⣿⣿⢲⣷⣷⣿⣷⣺⡠⡴⢂⡀⠠⠈⣉⠀⠀
⠀⠚⠛⠿⣸⠿⣿⣿⣧⣿⢸⣿⣗⣯⣴⣶⣿⡟⠃⡟⣿⣿⣷⠆⣷⣟⣻⣽⣺⢗⣯⡇⡇⢺⣿⣿⣿⣿⣷⣿⣿⡿⠿⡷⣿⣿⣿⢀⣿⣿⣇⣿⣿⣿⣸⣿⣿⡇⡿⣿⣿⢿⢸⣼⣯⣥⣼⣟⣿⠯⠖⠂⠀⠀⠁⠀⠀
⠀⠀⠀⠀⣷⡶⣿⠿⢿⣿⣼⣿⢿⣿⣿⣿⣿⡗⢀⣇⣿⣿⣿⣾⣿⣿⣙⣼⣼⣁⣦⡇⣿⣿⣿⣿⣿⣿⢱⣯⣭⣵⣶⣩⣹⣿⣿⢈⣿⡟⡏⣿⢿⣿⢽⣿⣿⡷⣿⣿⣿⣿⢸⣿⣿⣿⣝⡟⠓⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠈⠉⠋⠈⠛⠁⠚⠚⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠑⠛⠊⠉⠉⠉⠛⠚⠛⠉⠉⠉⠋⠉⠉⠉⠃⠀⠀⠉⠁⠁⠈⠁⠀⠀⠉⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''',0.5)
def dragon_art():
    echo('''⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣉⣭⣿⣋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣿⣿⣿⣛⠿⠛⠉⠠⠴⢾⠿⣻⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣦⣄⣈⣥⣩⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⡋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣵⣶⣷⡿⣿⣿⠿⣿⣿⣿⣿⣿⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⣾⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡶⣒⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣾⣦⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣅⢻⣧⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡭⠝⢿⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣸⣿⡇⣿⣿⣿⣿⣿⣿⠿⣋⡛⣿⣿⣿⣿⣿⣿⣿⡇⢸⢿⣧⠹⣿⣿⣿⣿⣿⣿⡿⢿⣿⡿⠿⣿⣿⡇⣿⡿⢨⣿⣿⡿⢿⣮⣻⣿⣿⣿⣿⣿⣟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢋⣾⢋⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣾⡿⣿⣿⣿⢸⣿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡻⠷⢶⣯⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣸⡿⢣⣿⣿⣿⣿⢟⣵⣿⣿⢁⣿⣿⣿⣿⣿⣿⣿⣿⠸⡇⣿⣇⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡧⠀⣡⡝⣾⣿⢿⡿⣟⣿⣿⣿⣿⣿⣿⣿⣿⡽⠿⣿⣿⣿⣿⣿⣿⣿⡿⣡⣿⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣌⠉⢻⣿⣧⡈⢿⣿⢸⣿⡿⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡛⠛⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣯⣭⣽⣿⣿⠿⠇⡎⡿⢣⢈⣵⡌⡿⢋⣾⣿⣿⢣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣇⢷⠸⣿⣿⠈⠻⣿⣿⣿⣿⣿⣛⣿⣿⣿⣿⡇⣿⡇⣆⢹⣧⢸⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⣥⣾⣿⣿⣿⣯⣿⣿⢏⣼⣟⠉⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⣷⣎⠻⣿⣿⣷⠼⢸⣿⢷⠆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡿⣿⢟⣭⢹⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣿⣿⣿⣿⣿⣿⣿⣏⣴⡆⢰⣿⣿⡅⣿⣿⠇⢇⡿⣿⣿⢏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠸⡆⣿⣿⣧⠹⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣿⢸⣿⡘⡎⠿⠘⣿⣿⣿⣿⣿⣿⣯⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⢿⡿⣣⣾⡟⢨⠞⣽⣿⣿⣿⣿⣿⣿⣿⡷⢿⣿⣿⣿⣿⣿⣿⣿⡘⣿⣿⣧⠻⣿⣿⣿⢸⣿⡧⡇⢽⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣁⣻⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⢀⣾⡽⣿⡁⠻⠟⢀⣾⣿⣹⡿⣸⣿⡿⣛⣿⠿⠿⣿⣿⣿⣿⡇⣄⢳⣿⢹⣿⢻⡼⢡⣶⣭⡙⣿⣿⣿⣿⣿⡿⢸⣿⡇⢷⢸⡖⣿⣿⣿⣿⡿⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⡟⣳⣾⢡⠏⠟⡀⣤⣾⣿⣿⣿⣿⣿⣿⠟⠉⣶⣾⣿⣿⣿⣿⣿⣯⣿⡇⢻⣿⣭⣧⢻⣿⣿⢸⡿⣷⣿⢸⣿⡿⠿⣿⣿⡿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⢜⣵⣿⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣿⠇⢸⣿⣷⣿⣯⣄⣁⣼⣿⣿⣿⢁⣿⡿⣰⡿⣹⣾⠃⢹⣿⣿⣿⣇⢿⡜⡿⣇⢿⣧⢣⣿⣿⣿⣿⣌⢿⣿⣿⣿⡇⠺⡛⣿⢸⠀⣧⢸⣿⠟⣡⣾⣿⣿⡄⣿⣿⣿⣿⣿⡿⢋⣾⡿⣋⣴⣯⣶⡧⢿⣿⣿⣿⡿⠿⣋⣵⠞⠻⠼⢿⣿⠛⡛⢿⣿⣿⣷⣿⢰⢻⣿⣟⡈⣿⠟⢚⣷⣾⣷⢨⣿⣿⡷⡉⢿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢩⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢷⡟⣜⣾⢋⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢸⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⣾⡿⠱⠿⠃⣿⡇⠀⠘⢿⣿⣿⣿⢸⣿⣧⣿⠜⣿⣎⢿⣿⣿⣿⣿⣧⠙⣿⣿⠀⣾⣿⣿⡆⡇⠿⡾⣫⣼⣿⣿⣿⣿⠃⣿⣿⡿⠋⣩⢴⡿⢋⣰⣟⣿⣿⣿⣿⣭⢻⣿⣿⣿⣿⣿⣿⣿⣷⠸⣿⡿⢸⣷⡸⣿⣿⣿⣿⣘⣸⣿⣧⣧⠷⢲⣿⣿⣿⣿⠸⡏⢻⣇⢃⣷⡻⣷⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡛⢻⣿⡿⠿⢿⣿⣯⡙⣙⢻⣏⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣿⣽⣾⣿⣿⣿⣟⣛⠟⠋⠁⠀⠀⢀⣉⣬⣁⠀⠈⢋⣻⣿⡟⠛⠒⠲⢿⣬⣿⣛⠿⣦⣿⠽⣄⣿⣿⣿⣿⣿⣷⡍⠟⣼⣿⣿⣿⣿⡟⣠⣶⣿⣿⣿⣿⣿⡇⣸⡿⣉⣰⣴⣿⣿⢇⣿⡏⣮⣻⣿⣿⣿⣿⣆⢻⣿⣿⣿⠿⣿⣿⡟⢰⣿⣧⠀⢿⣷⣮⡛⢿⣿⣿⣿⣿⣿⣿⣷⣾⣟⣿⣿⣿⢂⣴⣿⣿⣿⡸⣷⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡽⣷⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣟⣒⣻⠋⠛⣿⣿⣿⣦⣝⣋⣟⣊⢸⢟⣣⣿⣻⣶⣘⣋⣋⣵⣶⣾⣿⣿⣯⣿⣿⣿⣿⣿⡿⠋⣩⣼⣿⣿⣿⣿⣿⣿⣿⡟⠉⣀⣤⣶⣾⣿⣿⠻⡿⣿⣿⠟⣉⣥⣤⣤⣾⣿⣷⣶⣿⣿⣿⣷⣮⡛⡄⣿⡟⡿⣿⣿⣿⢟⣁⣼⣿⣿⣿⣿⣦⣿⣿⣿⣿⣿⣿⣿⣿⢁⣿⡷⠳⣿⠟⠏⢁⣿⣿⠿⠋⠱⠶⠭⠬⠇⠿⠷⢶⣿⣿⣿⣿⡗⠀⠘⠿⠿⠇⠀⠈⠙⠻⠎⢿⣿⣿⣿⣿⣿⣿⣿⣎⡻⠟⠟⣾⣿⣿⣿⣛⡃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠻⣿⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣷⢱⢻⣧⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⠠⣜⢿⠻⣁⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣋⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⣿⣿⣿⣿⣿⡿⠃⠨⠖⣛⠁⠊⢀⡩⠟⢷⣌⣻⣿⣿⣿⣿⣿⣿⣿⣿⣇⠁⣿⣘⣹⣿⣿⡾⠟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠘⢫⣄⣼⣶⣿⣿⣿⣥⣴⣾⣯⣶⣦⣀⠀⢼⣿⣿⣷⣶⣶⣶⣶⣶⣾⣿⣿⣷⣾⣶⣤⣀⠠⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣮⡽⠡⢿⣅⣿⣿⣿⣿⣟⡻⣿⣿⣿⣿⣿⣷⣄⠳⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣡⣾⣿⡸⣸⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⠟⣻⡿⠛⠋⢽⣿⣿⣿⣿⣿⣿⣿⣿⣧⣛⠿⠟⢩⣉⣩⣍⣻⣿⣿⣿⣿⠟⣛⡏⣵⠟⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢣⣿⣿⣿⣿⣿⣿⠃⢠⢺⣿⢿⣑⠦⣿⣿⡿⠿⠟⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣚⣡⣴⣿⣾⣿⣿⣿⣿⣷⣝⠛⠛⠻⠋⠛⢿⢘⡄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢓⣴⣿⣦⡙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢿⣿⣿⣦⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⠛⢿⣿⣿⣿⣿⢿⣘⣿⣿⣿⣿⣿⣿⣷⣦⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⣦⣘⡛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠃⣛⠛⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣟⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⡿⠛⠿⠗⠀⠒⢹⣿⣿⣷⣿⣿⣿⣾⣿⣿⢟⣥⣤⡌⢿⣿⣿⣿⣿⣿⠏⣁⣾⡿⠧⠻⠀⣿⣿⣿⣿⣿⣿⣷⣿⣿⣛⣿⡷⢾⣿⣿⣿⣿⡿⣋⣴⣾⣧⢻⣿⣮⣓⠤⠘⠵⢶⡦⣶⣶⣿⣿⣿⣿⣿⣿⣿⣷⣌⢻⣷⣶⣭⠻⠿⠿⠿⢿⣿⣿⣿⠿⣛⣿⣶⡶⣒⣠⣶⣌⢻⣶⣿⣾⣿⣟⣻⡿⡿⠶⢦⣤⣀⠛⠛⠋⠉⢡⣲⣶⣦⣉⢻⣿⣿⣿⡻⢻⣿⣿⣿⣷⣽⣿⣿⣿⣦⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣟⣿⣷⣎⢻⣶⣶⣬⠒⠻⣿⣿⣿⣿⣿⣿⣿⡿⢱⣷⣭⣽⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⠟⣁⠀⣚⠹⣪⡄⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⠿⣟⣫⣽⣿⣞⣛⣿⣿⣿⣅⢀⣉⣉⣡⣤⣴⣾⣿⣯⣹⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⢯⣥⡀⣽⣥⣀⣉⠡⢚⣋⣥⣖⢆⣴⣦⠨⣽⡻⠷⠿⣿⣿⣿⣿⣿⡟⠳⣶⣿⣿⣿⣷⣾⣿⣇⢿⣿⣿⣭⢻⣿⣿⢫⠁⠤⣍⢉⣛⠿⠿⠚⠳⠿⣿⣿⣿⣿⣷⣽⣿⣿⣶⣴⣾⣿⣷⣬⣠⣴⣾⣿⣿⣿⣾⣿⣿⣶⣶⠆⢹⣿⣿⣏⣉⣹⣷⣶⣤⡬⠘⢉⣰⣶⣿⡷⠸⠿⢮⡝⣿⣶⡝⣿⣟⢿⣮⠻⣿⣿⣿⣿⠟⢫⠙⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⠻⣿⣿⣾⣤⠨⡛⡛⠿⣿⣿⡿⢱⣿⣿⣿⣿⣿⡟⠻⣿⣿⣿⡿⢟⣭⣶⣶⣾⣿⣿⣿⢿⡿⣋⣡⣞⡷⣿⣮⢳⢹⣾⢻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣾⣿⣿⣿⣿⣶⣿⣿⣒⣾⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣋⣭⣿⣿⣿⣿⡆⢿⣿⠻⢻⡇⣿⣿⣿⡇⢰⣿⡟⣿⣵⣞⠿⣛⠀⠉⣛⡿⢿⣶⣶⡘⢿⣿⣿⣗⡙⢿⣟⠻⣿⣿⣿⣿⡎⠿⣿⣿⣦⣙⢿⣿⢿⣿⣶⣄⣈⠧⢿⣿⣟⣣⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣁⣶⡶⠿⠛⠉⠅⢁⣂⡰⣿⣷⣶⢟⡻⠽⣞⡲⣿⣿⣶⣖⠸⠟⣡⣿⣿⣿⣿⣦⣭⣿⠿⠿⣿⠾⠷⠟⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠙⠿⢿⣿⡟⢠⣾⣷⡝⢻⣿⡯⠿⢿⣿⠿⢛⣵⣶⣬⣿⣿⣾⡿⣛⡽⠿⢿⣿⣿⣶⡾⠇⣴⣾⣿⣾⡿⣻⡶⣬⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣯⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⠿⢰⢸⣷⢾⣿⠉⣵⣿⣿⣷⣿⣿⣧⣤⣿⣷⠀⢺⣿⣿⡿⢿⣿⣾⣿⢾⡿⠿⣋⡉⢰⣗⠯⡲⢿⣿⡠⢬⣭⡙⠿⠓⠉⠳⣿⡻⢿⡿⠿⢦⡻⣿⣾⣇⠺⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣴⣿⡿⠟⢁⡲⠶⣶⣶⣦⣜⣣⣼⣿⠏⣩⣾⡿⠃⣵⣿⣿⣿⣍⣾⢀⡹⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠺⢿⣿⢿⣿⣿⣿⣿⣿⣿⣿⡿⡏⣻⣿⣟⣩⠝⢀⣠⣲⣮⠉⣄⣈⠙⠿⡿⠶⣥⣶⡆⠋⣥⣿⣿⣿⣿⣯⣿⣿⣿⣾⣽⣾⣿⠆⣻⠿⠋⢃⣀⡻⢿⣿⣿⣾⣿⡿⠿⠿⢸⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣧⣴⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣧⠘⢟⣰⣶⣿⡂⢻⣿⣿⡞⢿⡄⠻⢿⣿⡿⣷⣬⣻⠿⣭⣅⣙⣿⢿⣧⢨⣽⣿⣷⣆⣙⠿⣴⠭⢝⠿⣶⣮⣝⠳⡄⠀⢠⣽⣧⠀⢸⣯⣠⡶⡝⢿⣷⣅⢳⣮⡛⢿⢸⣿⢩⡿⢿⡟⣿⡟⢻⣿⣿⣿⣿⠋⣡⣿⣿⣯⠴⠶⣺⣿⣼⣿⣯⣴⣿⣿⠛⣵⣿⣿⣿⡏⣸⣿⣿⣿⣿⠿⢁⣶⣶⣿⣿⣿⢿⣿⡿⠿⠟⣛⣭⣿⢡⣨⣭⣛⡛⢻⡝⣿⣿⣿⡿⢋⣵⣤⣶⣾⣶⡿⠟⢋⡭⢹⣿⣿⢿⣎⢻⣿⣱⣪⣭⣄⢶⣷⠆⢤⠹⣭⣭⣽⣯⣭⣭⣭⣝⠿⠋⠁⣀⡻⣿⣿⣿⣿⣿⣦⢹⣿⡻⣏⠐⢲⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⢻⣧⠠⡙⢹⣎⡻⣆⠙⣿⣧⢋⠿⣦⡂⠻⢿⣝⡿⠿⢿⣾⣿⣿⣿⣿⣷⡺⢮⢙⣻⣿⣿⣿⣾⣥⣄⣀⠂⠉⣿⡿⠆⢠⣿⣿⠁⡀⡉⢻⣿⣧⡶⣧⠹⢹⣦⠹⢫⣦⠀⠉⠘⣛⠛⠃⢿⠃⣠⡾⠟⠉⣠⣿⣿⣿⣿⣿⣿⣿⠸⢋⡍⠹⣿⣿⠟⢡⡆⡟⠱⠿⠟⡀⢹⣯⣷⡶⣂⣴⢈⣿⡯⣻⣽⣷⣶⣿⣿⣏⣍⣽⠟⣱⣬⣿⣿⣯⣭⡻⢿⣮⠽⠿⢾⣿⣭⣽⣿⡷⠶⣷⣶⠀⠀⠀⣁⣽⠿⣿⣥⣽⣿⣿⡻⣿⡇⣿⡇⢾⡷⠈⣿⣜⣿⠻⣿⠿⢎⣆⠻⡷⣿⣿⢨⡿⣿⣿⣿⡷⠈⡿⣧⣿⣿⣿⣿⣿⡿⣿⡿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣋⢀⣿⡄⢻⡿⣮⡄⢸⣿⣷⣬⣿⠟⣷⣬⡻⢿⣿⣿⣷⣿⣮⣟⣟⣯⣷⣾⣿⣿⣯⣥⣉⠋⠛⠛⠛⠉⠀⠛⢁⣶⣼⣿⣿⣇⢳⣿⣾⡁⢿⣦⠙⠛⠈⠉⠀⠈⠑⣠⣾⣿⣿⣿⣧⡐⠆⠉⠀⠈⢿⣯⣉⡻⠿⣿⣽⡿⠛⠀⢈⢣⠀⣿⢿⣿⣾⡇⢠⠈⣉⣉⣩⣉⣵⣶⠿⣛⣭⣾⣿⡿⠿⠿⠿⠟⠿⣿⣿⡿⣫⣾⣿⣿⣿⣿⠛⣿⣿⣴⣾⣿⠸⢿⣿⣿⣧⣴⡶⣶⣾⠟⡀⠈⢙⣻⣿⣿⣿⣿⣿⣿⣿⢻⣏⣼⣿⡿⣦⣽⡇⡘⣿⣿⣧⣿⣿⣿⡿⠘⣿⣿⡏⣿⡇⣿⣿⣿⡿⢄⣷⡀⣿⣿⣿⣿⣿⣏⣛⣻⡿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣧⣝⣛⣛⣯⣝⣻⣿⣿⣟⢸⣿⣿⡜⢳⣾⣷⡀⢻⣿⠿⣿⣿⣿⣿⢿⠑⠹⢿⣛⣻⣿⣇⣿⡟⡡⠚⣩⡄⠙⠷⣿⣽⣿⣿⣿⣿⣿⠟⠸⣿⡿⣿⣿⣿⣷⠀⢀⠀⠠⠤⣤⣄⣤⣿⣿⣶⣾⣿⣿⣿⣿⣿⠟⢀⣶⣶⣦⡀⠈⠙⠛⠻⠿⠛⠉⣄⡰⣶⣿⡾⢸⣿⣿⣿⡟⣃⣀⠀⠙⠿⢟⣿⣟⣛⡃⠛⠛⠉⠁⠒⢂⣠⣤⣾⣿⣿⣷⣽⣿⣿⣟⣻⢿⣷⣿⣽⣿⣻⣿⡇⣼⣷⡽⢿⣿⣿⣿⣿⣿⣷⣤⣾⣿⣿⣿⣿⣿⠿⣿⢗⣵⢟⣼⣿⣿⣿⣦⣽⣱⣿⡞⣿⣿⣿⣿⡝⢁⣼⣿⣿⣷⠸⢷⠹⣿⠏⢡⣿⣯⡄⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣻⣿⣿⣿⣿⣴⣿⣿⣇⢸⣿⣻⠃⢸⣿⣿⣇⠘⣿⣇⡘⣏⢋⣿⣿⣿⣿⣦⣮⣙⣛⠛⠟⠠⢤⣦⣾⣤⣿⣷⣦⢝⡛⠿⠿⠋⢡⣄⡀⠈⠰⢟⢛⣉⣤⣿⠎⣿⣿⣷⣮⣝⠻⢿⣿⣿⣿⡿⠿⢿⣿⡋⢼⣿⡿⢟⣛⣓⣀⠻⣿⣷⣦⣤⣤⣌⡙⢓⣊⣤⣿⣿⣿⣯⣾⣿⡏⣰⡀⣴⣤⣉⣛⡛⠿⠿⣛⣛⣛⣯⣬⣥⣴⡿⠟⢠⠭⠹⠛⠛⠛⠿⠛⠿⠿⢿⣿⡿⠟⣰⣿⣿⣿⣜⢿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣥⢞⣵⣿⣿⣻⣽⣿⣯⢏⣿⡟⢿⣟⣻⣛⠛⠥⣼⣿⣿⣿⣿⠃⡸⣿⣿⡇⢸⣿⣿⡇⠿⠟⠛⠉⠉⠛⠟⠻⠟⠻⡿⠿⠿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣶⣿⣿⣿⣿⣿⣿⣿⢟⣿⣥⡸⣿⠇⣰⡀⣿⣿⣿⠀⢻⣿⡟⣜⠛⢿⣿⣿⠿⣿⣿⣿⠋⠤⠜⢲⣿⣯⣵⣷⣽⣿⣿⣿⠿⣿⠄⡆⣦⣟⢿⣶⣸⣿⣿⣿⢟⣵⣦⠻⣿⣿⡟⣿⣿⣦⢹⢿⣿⣿⣶⣤⡆⢁⣤⡄⣤⣾⣿⣿⢟⣦⡹⢻⣿⣷⣌⢿⣿⣦⣀⠛⠿⣯⣕⡈⠉⠟⢠⣿⣇⢻⣿⡏⢻⠟⣿⣿⣿⣿⣿⣿⠿⢛⣋⠠⠤⣀⣀⣀⡀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠉⠋⢸⣿⣷⡝⢿⣷⣾⣯⣽⣿⣷⣿⣻⣿⢛⣭⣷⡚⣻⢆⣬⣭⡢⡙⣡⣼⣏⣸⣭⣽⣯⣬⣿⣾⣷⡭⢽⠛⣩⣤⣿⣿⡟⣡⠘⣿⡿⠀⠀⠀⣠⣄⣀⣄⡀⠀⠀⢀⣒⡉⣍
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣛⣻⣿⣿⣿⣿⣿⣿⣿⣯⣷⣿⣿⣿⣿⣿⣛⣛⣩⣿⣿⡿⠿⠃⠤⣼⣧⣧⠹⣿⣿⡄⠀⢿⣇⣿⣷⡀⣿⣿⢀⣿⣿⠇⣴⣷⣿⣿⣿⡿⠾⣿⡿⠟⢋⣉⣇⡍⣾⣿⣿⠋⡃⣹⣿⣿⣿⢇⣾⡟⣱⣷⠹⣿⣧⣿⣿⣿⣼⣿⣿⣿⣿⡿⢰⣿⡿⣹⣿⣿⣿⡣⣾⣿⣿⣆⢿⣿⣿⣤⣈⢻⣿⣿⣿⣶⡌⣡⣾⣷⡖⣸⣿⣇⢻⣷⣘⢦⠛⠛⣛⣻⣏⣠⣌⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⡀⠀⠀⠀⠀⠀⢻⡟⠿⣦⠹⣿⣶⣿⣿⣿⡏⢁⣴⣿⣿⣿⣷⣹⣟⣿⣿⠟⣡⠛⣛⣉⣿⣿⣿⡿⣽⣿⣿⣿⣿⡟⠤⢹⣿⣿⣿⡇⠀⠀⣙⣃⣴⣿⣿⠛⡫⠉⠀⠀⢤⡼⠿⢛⣛⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣷⠾⡿⠿⠟⢉⣉⡄⠆⢉⡍⣰⣿⣿⣿⣇⢻⣿⣧⢰⣄⢿⣶⣿⠙⣼⣿⡎⣿⣿⠐⣛⣻⣯⣍⣥⣤⣾⣷⣦⣌⣸⣿⣿⣷⡼⢛⣡⡾⢡⣿⣿⣿⣟⡆⡜⣼⡟⢙⣰⠝⣿⣿⣿⣿⣼⣿⣿⣿⣿⢣⣾⣿⣶⣿⡿⢻⣿⢡⡹⡿⣿⣿⣧⢻⣿⣿⣿⣷⣼⣟⠻⠇⣿⣿⡟⠁⢾⣿⣿⣿⣧⣻⣿⡰⠶⣤⣈⠿⣿⣿⡟⣼⣿⣿⣿⣿⢿⣿⣿⣿⣿⢿⣮⣿⣦⠀⠀⣱⣶⣾⣲⣶⣾⣧⠀⠐⣿⣧⡍⢉⣀⢸⣿⣷⣶⣾⣿⣿⣿⣿⣿⣿⠟⣁⢘⣻⣿⣼⣿⣯⡿⢟⣄⢹⣿⣿⣿⣿⠀⠀⠘⣿⣿⣿⡇⣤⣼⣿⣿⣟⣛⣚⣡⣤⣶⣤⣦⣶⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠉⠀⠀⠈⠉⠀⠀⠐⠓⠉⢕⣶⣾⠛⣡⣛⣟⠻⢿⣿⣆⠻⣿⠠⠕⠈⣿⣿⡀⠸⣿⣿⣞⢻⡈⢙⣽⣿⣿⣿⡿⠿⢿⠟⣷⣯⠟⠋⣡⠶⠒⠋⣴⣿⣟⡛⢿⡏⢰⣿⡿⣡⣿⠫⣠⢻⣿⣿⣿⣿⣯⣭⢹⣻⣿⣿⣿⣿⢏⡄⢈⠻⣿⣿⣿⣽⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⡄⢹⣿⣷⠸⣦⡙⠛⣿⣿⣿⣼⣿⣷⣾⣿⣶⣤⣶⣶⠄⣩⣥⣤⣾⣿⣿⡿⢻⡷⠘⣿⣿⣿⣷⠿⠿⢿⡛⠡⠹⠟⠡⠁⠀⠒⠂⠀⠠⠴⠆⢻⣿⣿⠻⣿⣿⠟⢿⣿⠃⠀⣿⣿⣿⣿⡿⡳⠋⠴⢋⡉⢰⣿⣿⣿⠏⠀⠀⠀⢹⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣿⣿⣿⣿⣿⡏⣀⣠⣤⣄⣤⣤⣤⠤⠆⠀⠈⠉⠛⢊⠔⢹⣿⣿⣿⣦⡙⣿⣦⣨⣤⣶⣧⢻⣿⣇⣧⠹⣿⣿⣄⢣⠈⠚⠛⠶⣲⠲⢁⠀⣠⣄⣊⣴⣚⣷⣿⣷⣿⣿⡿⠿⣛⠸⢃⣿⠏⣾⣿⣯⡄⣽⠎⣿⡟⡎⢴⣿⣿⣷⣙⢻⣿⣿⢇⣚⠋⠚⠆⣿⣿⣿⣗⢿⣿⣿⣿⡹⣿⣿⣿⣿⣿⣿⣾⣿⣿⢧⣓⠚⣶⣦⣍⠛⢯⠹⠿⠿⠚⠛⠛⠥⠊⣾⣿⡿⡿⣿⣿⠖⠒⠉⠀⠴⠟⡁⠿⠋⠐⠂⠀⠀⠀⣠⡀⠀⠈⠀⢠⡄⠀⠀⠀⠀⠀⣿⣿⣄⣿⡖⣰⡾⢁⡆⣶⣿⣏⣿⣿⡖⢡⣾⣶⣶⠆⣾⣿⣿⠟⣼⣷⣯⣴⡘⣿⡟⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⡿⣿⣯⣄⣠⣤⣦⣤⠄⠜⣋⡼⢹⣿⣿⣿⣿⡇⢹⣿⡿⠿⠿⠿⡅⢿⣿⠀⡀⢙⣿⣿⣎⣆⠀⢀⣀⡀⠀⠀⠀⠻⣟⣛⣛⣛⣛⣫⣭⣶⣶⢨⣿⣿⡀⠘⡏⣼⣿⣿⣿⣿⣇⣡⢉⠈⡵⢐⣿⣷⣤⣈⡙⢿⣯⣾⣿⣿⣿⣿⣿⣿⣿⡎⡞⣿⣄⢹⣿⣌⢷⣿⣻⣿⣟⡿⣿⣿⣿⣿⣤⣈⡛⠱⢧⣍⠣⠾⢿⣟⠁⠀⠈⠛⠒⠬⠟⠅⠛⠉⠯⠌⠤⠖⠚⠃⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠾⣿⣿⣿⣶⣼⡇⣿⡏⣵⣿⣼⡿⠁⢦⡆⣿⣿⣿⣿⡟⣠⣿⣿⣿⡟⣰⣿⣿⠟⣰⣿⣿⣿⣿⣷⣌⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠉⠉⣛⣫⣽⠿⠿⢿⣿⠿⠋⠉⢁⡎⣾⣿⢇⣿⣿⣡⣿⣿⡇⠸⣶⡶⠾⠷⠛⣃⠈⠉⠀⠁⠀⢛⣿⣿⣿⡐⠛⠋⣁⡠⠚⣀⠀⠈⠻⠿⣿⣿⢿⣿⡇⠛⣾⡟⣯⠃⠸⣹⡿⠋⠈⣿⡟⢿⡿⠃⢤⡠⠿⠿⠿⢚⣯⣹⣷⣶⣦⣻⣿⣿⣿⡿⣿⣿⣿⡹⢹⣿⠀⣿⣿⡘⣿⣿⡟⣾⢿⣿⡭⣝⣻⡿⠿⣿⣿⣷⣦⣳⣶⡌⡛⠄⣐⣛⣛⡻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠶⠖⡈⠍⠉⠿⠛⢀⢏⣼⣿⣿⠟⣀⡐⠿⣦⣿⣿⣿⠏⠰⠿⢭⣿⡿⣱⣿⣿⠟⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⣭⢿⣿⣿⣷⣌⠻⠃⠈⠉⠉⠩⢁⣀⣀⠀⠀⠀⠀⠀⠀⣾⣦⣾⣿⣼⣿⣿⣿⢹⣿⡇⠠⠄⠀⠠⠤⠤⠾⠟⠂⠀⠀⠀⡈⢟⢿⣿⡇⠿⢟⣀⡀⢀⠐⠋⡀⣀⣀⠀⠉⠛⢭⣯⢸⣿⢸⣿⠀⠁⠟⢀⣴⣦⡿⠁⡟⠀⡀⣽⣷⣿⣿⣿⣶⡀⠙⢳⢹⣿⣿⣏⣿⣿⠷⠻⣿⣿⡷⠀⣻⡆⢸⣿⢧⢻⠟⢘⡳⣾⣿⣿⢆⣿⣿⡿⠶⣯⣻⣿⣿⣟⣻⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣴⣦⣶⣶⣶⡿⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠊⣸⣼⣿⣿⢋⣴⣿⣿⣿⢻⣿⣿⡏⣼⣷⣿⣿⣿⢁⣿⡿⣋⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠟⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠠⠄⠊⣥⡖⣶⣦⣄⣐⠛⠀⠠⣖⢠⣿⡏⢻⣿⣿⣿⣿⢣⣿⡟⢰⡒⠒⢒⠒⠒⣚⣢⣬⣤⣴⣠⣵⣷⠸⣿⣿⡇⢸⣿⠿⠿⢏⠀⣀⣈⡉⡉⠀⠀⣠⡦⠀⣸⣷⣿⡏⠀⣤⡄⢸⣿⡟⠀⠀⢀⡺⣿⣿⣿⣿⣿⣿⣭⣀⠏⣤⡼⢿⡟⣏⣿⣿⣿⣆⡹⣿⣿⠀⣿⢻⠗⣼⡸⠌⠞⢻⣿⣬⣭⣏⣾⣿⣿⡇⢈⣿⣿⣦⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠬⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠦⡤⢀⣨⣿⢿⡿⠁⠀⢹⣾⣿⠏⣼⣿⡏⣼⣿⣿⣿⣿⣿⣦⣩⣶⣿⣿⣿⣿⣿⣿⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢛⣛⣉⣩⣾⣿⠿⢟⣉⣡⣾⣿⣿⣿⣿⣿⣿⣿⡇⠶⣸⣿⠃⠘⢿⣿⣿⣽⣷⠌⣿⡜⣿⣧⣿⣿⣿⣿⡿⢸⡿⠑⢉⣀⠀⠀⠀⠀⠉⢩⣿⣿⡿⡿⠏⢁⡃⢻⣿⠣⠉⡀⢀⣴⣶⣾⣿⡟⠛⠃⠀⠀⢉⣴⠀⣿⣿⢟⡁⠸⣿⣧⡈⠋⠷⣿⣿⣿⣿⣯⣟⠻⢿⣿⣿⣿⣯⣴⣿⣿⣿⣿⡾⣿⣿⣿⣿⢇⣿⣿⣶⣿⠠⠾⠟⣁⣶⣿⣿⣿⡏⢽⣾⣿⣟⣿⣇⢺⣿⣿⣿⣿⡿⣷⠿⣿⠿⠿⠟⣛⡉⠉⢩⣥⡖⢰⣿⢰⣿⠃⠀⠀⠃⠀⠀⠀⠠⠄⠀⠀⠀⠀⠀⠀⠾⠿⠟⣡⣾⣿⣿⠟⠀⠛⠉⠋⠀⠉⢼⡿⠏⠀⠉⠉⠉⠈⠉⠙⠛⠙⠻⠟⠻⣿⡮⠯⠥⠄⠄⡈⠍⠋⠀⢁⡐⡻⠯⢟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣿⠇⠀⢠⣿⣿⣿⣿⡏⣼⣿⡇⣿⣿⣿⣿⣿⣿⡇⢺⢡⣞⣵⣀⣌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠽⠦⠴⠞⠉⠉⠁⣀⠀⣤⠭⠑⠂⠀⠀⣴⡿⠏⠰⣿⣿⣾⡇⠀⠈⢩⣥⣶⣿⣾⣿⡟⣿⣿⣿⢑⢶⣶⡆⢸⣿⣿⣿⠻⢮⣉⣋⣙⠻⢿⠿⣾⣿⣿⡿⡿⣰⡞⣿⣷⣿⣿⣿⣟⣳⣿⣿⣿⣿⣿⣿⡜⣿⣿⣭⣿⣿⣿⠁⠰⢤⣜⣾⣿⣿⡆⠀⠈⣤⣿⡏⣾⣿⢀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢀⣀⣠⣤⣀⢀⣴⣿⣿⣿⢋⣠⣀⡀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣈⣺⣦⣦⣤⣤⣱⣶⣶⣤⣤⣬⣷⣶⣾⣯⠵⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣾⠏⠀⢀⣾⣿⣿⣿⡏⢘⣋⣭⠠⠾⣹⣿⣿⣿⣿⡇⠃⠜⠛⠛⠛⠩⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠂⠀⠀⢀⣾⣿⣷⡐⠚⠛⠀⠀⣾⢟⣴⠁⣸⣿⣿⣳⡁⠀⠀⣼⣿⠙⣿⣿⣧⠆⣿⣿⡟⣾⣿⣿⢉⢸⣿⣿⡏⣤⢸⣿⣿⡿⣣⣿⡇⠙⠩⣾⣿⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣧⢻⣿⣿⣏⣿⣿⡇⣶⣶⣮⡛⠛⠋⢁⣤⣾⣿⠟⣼⣿⡏⠈⣀⣿⣾⣧⣶⣶⣾⣿⣿⣿⣿⣿⡿⠋⢁⣾⣿⣿⡿⠁⠀⠀⠀⠀⠳⢗⣇⡀⠀⣀⠀⠄⡀⠀⠀⠀⠠⠤⠄⠀⠉⠉⠉⠛⢿⡿⠛⠋⡽⠾⠵⢶⣾⣩⣿⣍⣹⣿⣿⣿⣿⣿⣽⣿⣿⡿⠿⠿⣿⣻⣭
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⡏⠀⠀⣾⣿⣿⣿⡟⣰⣿⣿⡟⡀⣾⣿⣿⣿⣿⣿⡇⣤⣤⣤⣤⣤⣴⣶⣶⠦⠀⠀⢀⣠⣤⣶⣤⣤⣴⠶⠒⠒⢂⠏⢹⣿⣿⡇⢸⡿⠋⢸⢏⣾⠃⢢⣿⣿⣿⣿⡆⠀⠀⠟⠁⡄⢹⣿⣿⠀⣿⣿⢣⣿⢺⣿⣿⢸⣿⣿⠀⢿⢸⣿⣿⣷⣿⣿⣥⣼⣤⣹⣿⢸⣿⢿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣇⢹⣼⣿⡌⣿⡏⡿⣡⠘⣼⣿⣿⣧⢰⣿⣿⣿⡏⡤⣽⣿⡅⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡖⢀⠸⣿⣿⠟⡱⠶⠀⠀⠂⠀⠛⠛⠛⠃⠀⣀⣴⣴⣔⣲⠞⠒⠒⠂⠐⠒⠑⣶⠦⠄⠀⠀⠁⠀⠀⠀⠀⠀⠊⠈⠛⠛⢻⣿⣿⣿⣿⣿⣿⣿⠿⠿⡿⢿⠿⠿⡿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠙⡟⠀⠀⣼⣿⣿⣿⡿⣱⣿⣿⣿⠁⢸⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣻⣍⡀⠀⠀⠀⠀⠀⠀⠁⢀⣒⣦⣤⣶⣶⣾⢇⠎⣰⣿⣿⣿⡷⠸⠡⠟⣫⡶⠛⣀⣿⣿⣿⣿⣿⣷⠂⠀⠀⠐⣢⣸⣿⡿⢰⢿⣿⡘⣱⣾⣿⣿⡘⣿⡇⡧⣼⢸⣿⣿⣿⣿⠋⢉⣭⣅⠻⣿⠸⠋⣾⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⡇⢙⡷⣀⢋⣰⣿⡋⣿⣿⣿⢿⣿⡟⣰⣿⣿⣿⢠⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⢁⠈⣉⣉⠀⠁⣭⡥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢀⣀⣀⣡⣤⡈⠀⠀⠀⠀⠨⣅⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⠀⠀⠀⠈
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠈⠀⠀⢰⣿⣿⣿⡿⣱⣿⣿⣿⡇⢰⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣯⣭⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡌⣼⣿⣿⣿⣿⡇⣡⣶⣿⣿⣿⣇⢿⣿⣟⣿⡿⠟⣫⣴⣶⣶⣶⣿⢿⣿⡇⠶⢸⣣⣴⣿⣾⣿⣿⣿⢿⢸⡇⢹⢸⣿⣿⠟⡅⣠⡼⣿⣿⠏⠀⠰⢠⣿⣿⣿⣿⣿⣴⣿⣿⣿⣿⣿⣿⣿⣶⡧⣿⣿⠃⣈⠛⢿⣼⣿⣹⣷⡚⢿⣿⣷⡙⢱⣿⣿⣿⣇⠈⡿⢿⠟⠃⠀⣠⣶⣾⣿⣿⣚⣩⣽⠯⠀⢩⡷⠂⠀⠶⣶⣦⣤⣠⣤⣴⣶⣶⣾⣿⣿⣷⣶⣶⣶⣶⣶⡤⠀⠉⠓⠀⢐⣋⠁⢀⠀⠀⠀⢠⣤⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠰⣿⣿⣿⣿⢡⣿⣿⣿⠟⠠⣾⣿⣿⣮⣯⢿⣿⣿⡇⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢀⣼⣿⣿⣿⣿⣿⡃⠨⣍⣭⣝⣛⣉⠘⣿⣿⣿⡁⢸⢫⡝⠻⣿⣿⣿⠇⣿⠓⠀⠐⠺⣿⣿⣿⣧⠙⢿⢄⣾⣿⠈⠀⣿⡇⣼⣾⣿⠃⠀⠀⣰⡿⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠹⢛⡱⣿⢇⠸⣿⣷⣟⡻⣿⣁⡟⢿⣿⣗⢝⣛⣿⡟⠠⢤⠄⣠⣤⣴⣾⣿⣿⣿⢿⣿⣿⣷⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠝⠿⠟⠛⠛⠋⠉⠠⠦⠶⠛⠁⠀⠀⠀⠀⠘⠉⠉⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣍⣛⣃⠿⠿⢋⣴⢏⣠⡝⣿⣿⡞⣿⣿⣿⣯⡁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠜⣿⣿⡟⣿⣿⣿⣟⣷⡼⣾⣿⣿⡿⡠⢹⣿⣏⠇⠸⣿⡻⣶⢿⣿⣿⣆⠟⠰⣸⣦⢀⣾⣿⣿⣿⣦⣀⡟⣋⣴⣦⣀⢸⡇⣿⡟⠉⠀⠀⠀⣽⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣇⣰⡈⢳⣽⡌⣧⡉⢿⡏⣿⣷⣬⠓⡲⣯⣝⣐⠬⣝⣃⠊⣉⣿⣿⡿⣿⣿⣿⣿⣏⣁⣄⣽⣿⡿⠿⠛⠛⠛⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠀⠀⣀⣀⣀⡤⠀⠂⣀⣀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⡏⣸⢿⣷⣿⣿⣿⢻⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢠⣾⣿⣿⢀⣿⣷⣿⣿⣿⡄⢿⡿⠙⠴⠋⣈⣽⣿⣾⣷⣝⠿⣦⡲⠿⣿⣿⣵⣾⣿⣿⣾⣿⣿⣇⣿⠟⣫⣾⣿⣿⣿⣿⡏⢡⣽⣤⡦⢀⣷⡀⠿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣿⡟⣿⢃⣛⣙⡋⣤⣈⠻⣿⣷⡄⢾⣿⣿⣿⣷⠺⢿⣿⣿⣿⣦⡙⢷⡠⣀⠘⠀⠄⣉⡉⠉⠉⠉⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠘⠋⠉⠉⠉⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡞⣴⣿⣮⡻⣿⣿⣿⡞⢿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢸⣿⣿⣏⣼⣿⣿⣿⣿⣿⣷⡜⣷⣌⣥⡞⠉⡀⢹⣿⢟⣩⢷⣄⣷⣌⣒⠺⣿⣿⣿⣿⠟⠥⣛⣩⣶⣆⢿⣿⣿⣿⣿⡟⢱⣿⣿⡿⢇⣼⡿⣷⡀⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡡⢨⣭⣯⡿⢭⡿⠷⢨⡛⠿⢿⣿⡻⣿⣿⡇⣿⣶⣤⣝⠻⣿⡾⠟⢛⣛⠀⠿⠯⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠄⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢱⣤⣿⣿⣿⣷⣜⢿⣿⣿⣸⣿⣿⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣠⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣷⣜⠿⢿⣥⣬⣵⣦⠛⡾⢱⢫⢸⣿⢹⣿⡇⢲⡶⣶⣶⣴⡚⢿⣯⣻⣿⣮⠻⠿⣟⣋⣴⡏⠡⣬⣥⣾⣻⠘⠿⣃⣉⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⡟⠿⣣⣄⠆⢿⣿⣿⣟⠀⠙⠚⠄⠨⠿⠶⡬⣇⣈⠻⢶⣿⣿⣟⣿⣇⢿⣷⣌⠀⠀⢄⡀⠤⠤⠤⢶⣆⠄⠰⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣶⣦⣀⣀⣀⣀⣀⣀⠈⠀⠀⠲⠤⠤⡤⢒⣂⣀⡀⠀⣂⣠⡄⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⣾⣿⣿⣿⣿⣿⢿⣿⣿⣿⣽⣹⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣔⢶⣶⣶⡄⣰⣿⠆⢸⡇⠎⠿⠇⠀⢻⣟⠦⠻⣿⣟⢿⣿⣿⡏⠀⠘⣹⣿⣿⡅⠈⣩⠟⣿⣿⣻⣌⠑⠿⢿⣿⣻⣿⣿⣿⣿⣿⣿⡟⢡⡤⣌⣙⡳⣄⠿⠟⠁⣫⣾⣿⠆⣿⠘⣓⠿⠿⠿⠗⠀⣿⣿⣿⣿⣿⠎⣿⣿⡄⠀⠀⠉⠀⠀⠁⠉⠁⠀⠀⣀⣀⣀⣀⣀⣀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠶⠿⠷⠦⠤⠶⠐⠀⠁⠀⠈⠿⠻⣿⣿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣶⣾⣿⣿⣷⣾⣿⣿⣿⣿⡿⠟⠙⠃⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⣿⣿⣿⠉⣿⣿⣯⠻⣿⣿⣿⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⠛⢰⡿⠋⠀⣿⣵⣿⡆⢀⠀⣌⢿⣷⣤⣽⣿⡾⣿⣿⣷⠄⠀⣿⣿⣿⠇⠈⠁⠀⣿⣿⡞⠩⢀⣿⣶⣾⣿⣟⢹⣿⣿⣿⡿⢀⣾⠿⠿⠯⣭⣈⡃⠀⣴⣿⣿⡿⢸⢿⢳⢹⣬⢻⡖⡆⠀⠘⠛⣿⢿⣿⡇⢿⣿⣷⠀⠀⠀⠰⢶⣿⣿⡶⠮⠉⠉⠉⠉⠁⠀⢒⠻⠏⠀⠀⣀⢀⣀⣮⠀⢄⣀⣀⡀⡀⠀⠀⡀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠉⠁⡀⠀⠉⠉⠉⠻⠿⠿⠛⠛⠋⣉⣛⠛⠉⣤⣴⣦⡆⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⣿⣿⣿⣿⣼⢻⣿⣿⣷⣾⣷⣝⣮⢿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⢸⣷⣷⡆⢸⡏⠛⠛⢋⣷⡝⣧⡙⠿⢻⣿⣿⣿⣿⠃⣴⢀⠛⠿⠟⠀⢠⠄⠀⣿⣿⣥⡀⣘⢿⣿⣿⣿⣿⠎⢿⣿⣿⢚⡵⣶⣶⡦⢰⠊⣭⣅⣸⣿⡟⣿⠁⠀⣠⣤⡄⢿⣎⢷⢇⠀⠀⠀⠹⣦⡹⣇⠀⢿⣿⡜⣷⣶⣤⣄⠺⣯⣤⣤⣤⣶⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡙⠓⠈⣉⣁⣥⣄⣀⠀⠀⠰⢴⠶⠶⢒⣒⣰⣟⣩⣟⣛⣻⣷⣮⣽⣿⣟⣿⣥⣤⣾⣿⣿⡿⢙⣭⣭⣭⡅⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⣿⣿⣿⣿⣿⣿⢃⡾⣿⣿⣿⣿⡿⣸⣿⣿⣿⣿⣿⣿⣮⡳⣽⢿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⢸⣿⡇⣼⣿⡔⠸⣿⣿⣿⣮⠻⣷⣶⡍⠻⣿⣛⢸⣿⠘⠀⠐⣿⣧⣠⡎⢁⣭⣯⣭⣥⣾⣷⣾⣿⣿⣿⣜⢸⠿⣵⠟⡕⢻⡿⣷⠋⡠⣿⣿⣿⣿⢱⡇⢰⣦⠸⣿⣿⣮⡛⣼⣧⡱⣀⠀⠀⠻⣧⠸⡄⠘⣿⣿⡹⣿⣿⢿⣿⣮⣙⠻⢿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡸⣿⣿⣿⣿⣿⣿⣷⣾⣿⣝⣞⠻⠿⠿⣿⡿⠿⠛⠋⠉⠉⠉⢉⣛⣉⣉⣉⣩⣭⣥⣴⣾⣿⣿⣿⣿⡇⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢜⣿⡿⣣⣾⣿⣿⣿⣿⣿⣧⣿⣿⡿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⡿⢰⣿⣿⣇⠐⣬⡛⠿⢿⣧⣌⠻⣁⣾⣿⠀⣼⣧⡆⣹⠀⡐⠚⣿⣷⡈⣿⣿⣿⣿⣿⢿⣿⣿⢿⣿⡟⣼⣶⡍⣿⠃⢹⣧⡇⡇⠁⣿⡿⣿⣿⠘⢋⣭⡉⢷⣶⣾⣿⣿⣜⣿⣿⣦⡁⠙⠶⢌⡁⡀⠀⠘⣿⣿⡸⢋⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠩⠤⠶⠾⣿⣿⠿⠿⠟⠛⢉⣁⣠⣤⣤⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠛⡛⠛⠉⠉⠉⠁⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣟⣼⣿⣿⣿⣿⣿⡋⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡸⣿⡘⣿⣹⣿⣿⣿⣿⣿⣷⡝⣿⣿⣿⣿⣿⣿⣿⡿⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⣇⡺⣿⣿⣿⡅⢸⣿⣿⣶⣿⣿⣿⣿⣿⡏⢰⣿⣿⣇⠏⢀⠠⢵⣿⣿⣇⢸⣿⣿⣿⣿⣾⣿⣿⣾⢏⣼⣿⣼⣧⠀⡁⢿⣿⣷⡇⡇⣿⣿⡻⣿⣦⠸⣿⣿⣦⣙⢿⣾⣿⣿⣭⣏⣿⡝⢦⡲⠀⠙⢿⣦⡈⠜⣿⣷⡀⣸⣷⡝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣀⣠⣤⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠈⠃⠀⠚⠃⡄⢀⣀⠀⢀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣍⣭⣿⣿⣿⣿⣿⣷⣅⠿⣿⣿⣿⣿⣿⣾⣿⢮⢿⣿⣿⣿⣿⣿⣿⣿⣎⢿⣿⣿⣿⣿⣿⢣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣰⣦⢸⣿⣿⢰⣟⣻⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣧⢸⣿⣿⣿⠀⢠⢤⣤⣬⣽⡯⠀⣻⣿⡿⣳⡟⣿⡿⣣⣾⣿⣿⣿⡿⣰⡟⢸⡿⡿⠣⢀⢌⢿⣿⣼⣿⡧⣈⣛⡛⠿⣧⡙⣿⡳⣿⣿⣿⣿⣶⠉⠈⡂⠀⠈⠃⠐⠹⣿⣷⠙⠋⢰⣿⣾⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠉⠁⣠⣴⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⠃⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣿⣿⣿⣿⣯⡙⠻⣿⡿⣿⣷⡜⣿⣿⣿⣿⣿⣿⣷⣥⣹⣿⣿⣿⢿⣿⣿⣿⣷⡝⣿⣿⣿⢇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣁⣴⣿⣿⢸⣿⡟⢸⣿⡿⠟⣃⣠⡶⠶⠙⠻⠿⠟⢛⣙⡉⢸⣿⣾⣿⡇⠺⣿⣿⣷⣤⣿⣿⣿⣿⠳⢿⠃⢛⣾⣿⣿⣿⣿⣿⣇⣿⡃⣾⢡⣷⣿⡜⡞⣦⢻⡿⣿⣧⢉⣛⡛⠷⣮⣙⡌⢿⣆⣍⣿⡿⠁⣴⣿⣿⣿⣝⠦⡀⠀⠈⢿⣷⡀⢸⣿⣿⣿⡼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡜⠛⠛⠻⢿⣿⣿⣿⣿⠿⠟⠿⠿⠿⠟⠛⠛⠉⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠁⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⡟⣿⣿⣿⣿⣦⡍⣿⣯⣿⣷⡙⣿⣿⣿⣿⣿⣿⣿⣿⣶⣝⣿⣿⣿⣿⣿⣿⣿⣧⡛⠋⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣡⣣⣾⣿⣿⣿⡟⣸⣿⣇⣦⣄⣆⢐⣠⣿⣗⣒⣦⠄⢀⣶⣾⣿⣿⣷⣽⡻⢶⡾⠀⠸⢿⣿⣿⣿⣿⣿⣽⣿⣵⠀⢿⣿⣿⣿⣿⣿⣿⡿⠏⣰⡇⣸⣿⣏⡇⣧⢿⣇⢿⣮⣻⡟⣿⣿⣷⣦⣝⡻⢆⠉⠛⠉⢀⣼⣿⣿⣿⣿⣿⣷⣜⢦⠀⠁⠻⣿⡜⢿⣿⣿⣿⣷⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⣿⣇⢺⣿⣧⣬⣤⣩⣥⣤⣠⣴⣶⣶⣮⣧⣤⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⠟⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⡇⣯⢢⡹⢿⣿⣿⣿⣿⣿⣿⣷⣌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣻⣿⣿⣿⣿⡟⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣣⣾⣿⣿⣿⣿⣿⣻⢸⣿⢇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⣿⣿⡿⣲⣰⣿⣿⣿⣿⣿⣟⣿⣿⡟⡟⠣⣾⣿⣻⣿⣿⣡⠛⣱⣿⢟⡀⢻⣿⢿⣄⡟⣸⣿⣷⡻⣿⣷⣻⣿⣯⣥⣤⣽⡢⠂⡛⢿⣿⣿⣿⣷⡝⣿⣿⣿⣟⢿⣶⣀⠀⠹⣿⣎⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⡼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣋⠾⠁⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⡈⡇⣿⣾⣿⣆⠻⣿⣟⣿⣦⢿⣿⣿⣧⡺⣽⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢠⣿⣿⣿⣿⣿⡿⠟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣭⣿⢸⣟⣴⡖⠪⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣵⣾⣿⣿⣾⣿⣯⣿⣯⢙⢿⣿⡇⠀⡀⠛⠁⠉⠉⣩⣴⣾⢟⠱⣿⡇⢸⡏⢸⡿⣷⠸⣿⣿⣧⢹⣿⣿⣿⣶⣽⣿⣿⣿⣶⣮⣤⡈⠝⢿⣿⣿⡟⣿⢿⣿⣷⡙⣿⡆⢄⠈⢻⣦⡻⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣳⣿⣧⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣟⣽⣿⣿⣿⣿⣿⣫⠖⠉⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣇⠹⣿⣿⣿⣷⣿⣿⡎⣿⣷⣿⡿⣿⣿⣿⡻⣷⣽⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠅⣿⣿⣿⣿⠿⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣉⣴⣿⣾⡘⣿⣿⡇⢀⠰⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡚⣿⣳⣾⣏⣹⣿⡷⣈⣰⠸⣿⠃⣀⣃⢀⣃⣦⢲⣿⣿⣿⡙⣰⡿⣿⡎⢇⣼⣧⢿⣧⢻⣿⣿⠀⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⡦⢤⣙⠻⣟⡻⣬⣿⣿⣷⣬⡻⣮⡳⣄⠹⢷⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⡿⣻⣹⣿⢯⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣾⣿⡇⣿⣿⣿⣿⣿⣿⣿⡸⣿⣿⣿⣿⣿⣿⣿⣾⣝⣿⣹⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⡟⣫⣴⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⣿⣿⣿⣿⡿⠇⢹⠏⠁⣦⡆⠘⢮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣝⣻⣷⡋⢿⣷⣞⣻⣀⡀⣰⣿⣿⣿⣿⠁⣿⣿⣿⣿⣇⣻⡇⣿⠇⡼⣿⣿⠸⣟⣧⢻⣿⠀⣿⣿⠙⢿⣿⣿⣦⣭⣻⣿⠟⠛⠿⢷⣜⠿⣾⣯⣭⣭⣭⣭⣿⣟⣦⣝⢮⣳⣄⠹⣷⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣼⣿⣽⣿⢟⡝⣸⡿⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣷⣽⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⡻⠿⣿⣿⣿⣿⠟⢀⣾⣿⣿⣿⡿⢫⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣴⣿⣿⠟⡫⠎⣿⣿⠟⣿⣿⢠⡊⠈⣠⣸⡿⢃⢠⡀⢦⣭⠻⣿⣯⣿⣿⣿⡿⠛⢿⣿⢛⣽⣟⡻⠋⢻⣿⡟⢫⡿⣿⡟⠀⣿⣷⡹⣿⣿⣤⡹⢿⣿⣿⣿⣿⣇⢁⣴⣷⣼⣿⣧⡟⢻⣇⠿⣦⢿⣿⣿⣿⣿⣯⣻⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣶⣭⣭⣛⠿⣿⣽⣿⣿⣿⣮⡻⣷⣌⠻⣶⡝⢿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⡿⣿⣿⢷⡿⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣿⢿⣿⣿⣿⠏⣰⣿⣿⣿⣿⠟⣰⣿⣿⣿⣿⣿⣿⣿⢿⡿⣿⣿⡿⢯⣿⠇⠞⣱⣿⡿⢃⠸⡿⠁⠀⣤⢰⠊⠁⢀⣾⣧⡙⡷⢏⣱⣶⣭⣭⣭⣽⢰⢻⣠⣿⠛⣿⡿⢀⡄⣻⡿⠷⢌⣵⡏⠿⢄⢿⣷⣿⢿⣽⣿⣿⣾⣿⣿⠻⢹⣿⣎⢿⣿⡏⣿⢿⣿⣯⠻⣿⣿⢸⣏⢻⣿⣿⣿⣿⣿⣿⣿⣯⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣦⣍⠻⡮⠳⡌⠿⠟⠛⠛⠛⠛⠻⠿⠿⠿⣿⣿⣿⡞⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣫⠽⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡻⠿⠏⢨⣿⣿⣿⣿⠋⢺⣿⣿⢿⣿⣿⡿⢟⣵⣿⠛⣉⣽⢰⣿⣏⢤⣿⣿⡿⠱⣿⡇⠀⡀⢃⣤⣾⣿⡿⠷⠍⣩⣭⣴⡟⣸⠁⣿⢧⣹⣿⣿⣇⢻⣿⠀⠈⢰⣿⣿⡦⠈⣷⡋⠻⢇⣀⡈⠁⢿⣿⣿⣿⣽⣿⢹⡿⠡⠾⠿⣻⣿⣼⣿⣿⣼⡜⣿⣿⡇⣿⣿⢸⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣷⣶⣦⣂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠿⢿⣿⣿⣿⠿⡿⠿⠿⠿⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣸⣿⣿⡿⣰⢠⣿⣿⣿⣿⣟⡿⢱⠟⡟⡷⣿⣿⣿⣸⣿⡇⣾⢿⣿⣷⠸⣿⣇⠾⣽⣿⡿⠟⣁⢶⣾⣧⣿⣯⣭⣴⡟⣶⡇⡘⣿⡿⣿⣿⣦⡻⣰⣾⣿⣿⡟⠈⢻⣯⣽⣧⣏⡉⠍⢀⠈⠿⢿⣿⣿⢟⠄⠴⢿⣻⣭⣽⣿⣿⣯⡿⣿⣷⡘⣿⡇⢿⣿⡸⣧⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣽⣿⣯⡟⣧⣤⣅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⠀⢨⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢰⣿⣿⡟⣡⣿⢸⣿⠉⢻⣿⢿⢁⠸⣰⠃⠰⣿⣿⠛⢿⢿⢁⣿⢸⢿⣿⠀⣿⣿⣷⣖⢶⢶⣿⣿⢸⣿⣿⡟⢻⣿⡿⣴⣿⣿⡁⢿⣿⡻⣿⣿⣿⣽⣿⣿⣿⣟⣷⣄⣿⣿⣿⣿⣿⣥⣤⣴⡘⠠⢉⣑⢯⣼⣷⣿⣿⣿⣿⣻⣿⣿⣧⠹⡟⣠⣜⠧⣮⡻⢁⣿⣧⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠤⠤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢠⣺⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣾⡟⣩⡾⢿⣿⠀⢿⣷⢸⣿⢸⣿⢸⣿⡇⣿⣿⣿⡇⠘⡞⣿⡇⠈⣾⡟⣦⣿⢸⣿⣿⣆⢻⣿⣿⣾⣟⢿⣷⣾⣿⡇⢿⣿⣿⡇⣘⣿⣿⣦⠻⣿⣿⣾⣮⡟⠻⣿⣧⣿⣿⣿⣿⣿⡿⠟⣛⣻⠿⠿⢟⣼⣿⣿⣿⣿⣿⡿⠹⣿⣿⣿⡷⠁⣿⣿⣷⡙⣷⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⣬⣶⣿⡏⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⢪⣿⣿⣿⣿⣿⣿⡈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠈⣽⠇⣹⣧⡶⣿⣇⢸⣿⡇⣿⡘⢣⣿⣿⡗⣿⡎⣿⣿⣆⢡⣻⡇⢤⡿⣧⣿⢿⣇⣿⣿⣿⣌⢿⣿⣽⣿⣿⡿⢹⣿⣿⡬⢿⣿⡇⣏⣿⣿⣿⣿⡈⠻⣿⣿⣿⣿⣶⡍⠻⣿⣿⡝⣭⣶⣿⣿⣿⣿⣿⣽⣿⣿⣿⡿⢛⣫⣴⠞⣛⣿⣭⣾⣆⣿⡝⣿⣿⣌⢷⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢗⡿⣫⣿⡟⡰⣧⠸⠆⠀⠀⢀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣮⡉⣝⡻⣿⣿⣿⠟⣋⣘⡛⠿⣿⣿⣿⣿⣷⠈⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣰⡏⣸⣿⠻⣧⡲⠙⡆⣿⣷⣿⣧⢻⣿⡏⢇⢿⣷⡟⣸⣿⣆⢿⣿⡎⣇⢹⣇⢸⣿⡈⢿⣿⣿⣆⢻⣧⣻⣿⣷⣿⣿⣿⠁⣴⣿⠣⢸⣿⣮⣿⣿⣥⣷⠌⠻⣿⣟⢿⣿⣄⢻⣿⣿⣦⣿⣿⣿⣿⣿⣿⣿⣿⠛⢁⣤⡨⣥⣴⣿⣯⣿⣿⣿⣿⣿⣿⣮⣿⣿⡠⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⡵⣫⣾⣿⡟⠀⠇⡏⠀⡀⠀⠀⠀⠙⠻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣘⠿⡵⢞⣛⣿⣾⣷⣤⣝⠻⣿⣿⣧⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢰⡿⡗⣿⡟⣷⡙⣿⣦⠀⣿⣿⡏⣿⢸⣿⣿⢸⣿⣿⣃⣿⣿⣿⡆⢿⣿⡜⣇⢿⣆⢿⣿⣴⡬⣛⠿⣆⢻⣇⢿⣿⣿⣿⡇⣶⣿⣿⡄⣿⣿⢻⣿⣿⢣⣿⣿⣶⣌⢻⡘⣷⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⡿⣫⣶⣰⣿⣿⣧⢻⣿⣿⣿⣿⣛⣿⣿⣿⡏⣻⣿⢻⣷⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣵⣾⣶⣿⣿⣿⣿⣿⣿⢟⣫⣵⠞⣫⣞⣽⢫⡿⡅⠀⠀⠃⠀⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣟⣏⡉⢿⣿⣿⣿⣜⢻⣿⣿⢻⣭⣛⡛⡁⢿⣿⣿⣿⣦⣝⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣸⡇⢷⡿⠇⢹⣿⡗⢦⡀⠹⣿⣿⡜⢸⣷⣿⡌⢻⣿⢹⡏⣿⣥⣿⣮⡹⣷⡹⣶⣻⣼⣿⡿⣿⣶⣽⡂⠳⡿⣷⡝⢿⣿⣿⣿⣷⣿⡇⢻⣿⢸⣿⢟⣿⣿⣿⣿⣿⣷⣄⣿⣿⣿⣿⣿⣿⣿⣿⡽⡿⣋⣬⣶⢲⣿⢻⣿⣿⡼⣿⣿⣿⣿⡏⣿⣿⣿⣿⠙⡉⠘⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣛⣫⣽⣶⣿⣿⣳⣾⢯⣾⢏⣾⠇⠀⠀⠀⠀⠀⠀⠈⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⠻⢿⣿⣿⡎⣿⠈⣴⣿⣿⠫⣷⡌⡿⣿⣿⣿⣿⣷⡄⠑⠻⣿⣛⣿⣻⣿⣿⢰⣿⡇⢸⣇⢀⠺⣿⣿⣟⣿⡄⠹⣿⣿⡄⠻⣿⣿⣾⢿⢸⣿⣼⣧⣿⣿⣷⣌⠻⢮⢿⣷⢹⣿⣮⣿⢿⣿⣆⠙⣯⡓⠴⣽⣿⣿⣿⣿⣧⣼⣿⢿⡟⣸⣿⣿⠠⢸⣿⣿⣿⣿⡷⠙⣿⣿⣟⣛⣫⣷⣾⣿⣿⣿⣼⣿⢸⣿⣿⣷⡞⢿⣿⣿⡇⠹⣿⣿⣿⣇⢏⣶⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣫⣷⣿⣿⣿⣿⣿⣿⣻⣾⡿⣳⣿⣻⣾⠇⡰⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣤⣓⢾⠻⣿⡿⢀⣿⣿⣥⡌⢿⡇⡇⠸⣿⣿⣿⣟⣿⡇⠀⣿⣿⣿⣿⣿⣿⢸⣿⠀⢸⣿⣮⡀⣿⣿⣿⣽⣿⡆⢹⣿⣿⢧⣿⣿⢻⣾⢸⣿⡷⡿⣿⣿⣿⣿⣷⣜⠷⣝⡿⣿⣿⣼⣿⣿⣿⡰⡘⢿⣷⣮⣝⣿⣿⣿⡇⣻⣿⢸⡇⣿⣿⢇⢀⣿⣿⣿⣿⣿⣿⣧⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⡆⢿⣿⣿⣷⡘⣿⣿⣏⠁⠟⣿⡿⢋⣾⣿⡿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢀⣾⣿⣟⣷⣿⣿⡿⣻⣾⣿⢟⣽⡿⣱⣿⢃⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡔⣄⢀⠀⣿⣿⣿⣿⣿⡘⢱⣿⣦⠈⠙⠋⠉⠓⠀⠆⢻⣿⣿⣿⣿⡿⢸⡿⠀⢮⡻⣿⣧⢻⣷⡿⣿⣿⣿⡀⠹⡻⣿⡙⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢿⣿⣮⣛⠰⣽⣿⣿⣿⣿⡇⢳⡰⣝⡿⢿⣟⣿⣿⡃⣿⣿⣧⢳⣿⠋⣌⣸⣿⣿⣿⣿⣿⣿⣿⣿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠘⣿⢿⣿⣷⡸⣿⣿⣇⢸⡟⠀⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠄⣺⣿⣿⣿⣿⢿⣩⣺⣿⡿⢫⣿⡿⣹⡿⢣⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⢿⡿⠛⣫⣽⣶⣶⣜⢦⠀⣿⣿⣿⢻⠻⡇⢸⣿⣿⣧⣠⣀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⣿⣿⡄⢸⡇⢸⣿⡜⣿⣷⣾⣏⢿⣷⠀⡙⡸⣿⣸⣿⣷⣬⡻⣿⣿⣿⣿⣿⣿⣿⣷⡙⣿⣿⣷⣮⡛⠿⣿⣟⢿⣮⡻⡜⢿⣷⣿⠸⢧⡇⣼⣿⣿⣧⠿⠄⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢹⣯⢻⣿⣇⠙⡿⠋⣈⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣼⣿⣿⡿⣟⣵⣟⣾⣿⢟⣼⣼⣿⣽⣿⢡⣿⢱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣾⣯⣭⣍⣛⣛⣀⣴⣿⢟⣿⣿⣿⣿⣢⡃⠈⠙⡿⡟⠀⢡⣿⡿⢟⣛⣿⣻⣿⠂⠀⠀⠀⠻⣿⣿⣿⡇⢸⣿⡇⣇⢻⣼⣿⣿⣿⣿⣿⣽⣿⠻⣧⠀⣿⣌⠳⣻⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⠿⣿⣿⠯⠹⣿⣝⢿⣇⠈⣿⣿⣧⠈⣇⣿⣿⡏⣿⣿⣷⣄⠛⡻⢿⣿⣿⣿⡿⣿⣯⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⢷⣼⣿⡿⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢁⣾⡿⠟⣋⣿⣿⣿⣿⡿⣫⢟⣼⣿⣿⡿⣡⣿⢣⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣏⣟⣫⣭⣭⣭⣿⠄⠛⠻⣿⣿⢿⣿⣤⠀⢈⣧⣴⡿⠟⣱⣿⣿⣿⣿⣷⣆⢻⣦⠀⠁⠀⠙⢻⣧⡄⣿⣷⡘⣬⣟⠙⣿⡏⢽⣿⣿⣿⣷⢹⡆⣿⣿⣿⣮⠙⡿⠿⠿⡿⣿⡿⣿⡿⢿⣟⣛⣫⣭⣽⣾⣿⣿⣿⣿⡸⢿⣷⠹⠆⣿⣿⣿⣧⡻⢹⣿⢹⣿⣿⣿⣿⣿⣮⣔⣜⡝⠿⣷⣟⡿⣾⣿⣿⣿⣿⣉⣿⣿⣿⠿⢿⣿⠟⢀⢌⣁⣭⣶⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢋⣴⡿⢋⣤⣿⣿⣿⣿⡿⣯⣾⢫⣾⢿⣿⡿⢡⣿⡏⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⡟⡏⣨⡭⠿⣿⣿⠀⣀⣤⠹⠿⢿⣽⠿⣗⠀⣤⣤⣄⠀⠈⢹⣿⣿⣿⣿⣯⣷⡿⡇⠀⠀⠀⠀⠙⣧⠸⣿⡇⣿⡟⢀⢿⣿⣿⣿⡿⣿⣿⣷⠗⣿⣿⣿⣿⢰⣿⡆⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡘⣿⣿⣷⡼⣿⢿⣿⣧⠘⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡲⣬⡻⣧⣿⣿⣿⣿⡿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣥⣾⡿⢋⣴⣿⣿⣿⣿⢿⣯⠞⡩⣡⣿⢟⣾⡿⢰⣿⣿⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⡇⢷⠈⠈⠁⠈⢀⣠⣿⣿⠀⠀⢸⣿⣼⣿⣦⢹⡿⠿⠇⢿⡇⣿⣿⣿⠉⢫⣧⣿⠃⠀⠀⣠⡤⠀⢻⣇⢻⣇⢹⣇⢻⣧⣿⣿⣿⣿⡻⣿⢿⠀⢿⣿⣿⡟⣴⢋⣶⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢿⡇⣿⣿⡄⢿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣷⡟⣿⣿⡿⠋⣀⣢⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣴⣿⡿⣿⣵⣿⣿⣿⣿⣿⣽⣿⣽⡟⣽⣿⢫⣿⡟⠀⣼⣿⠁⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣷⣤⡔⢀⣠⣶⣬⣭⡛⢿⣾⣿⣿⡿⢿⣿⣿⣾⣿⣿⡇⡘⠿⣻⣿⡯⣄⠸⣿⣿⡧⠀⣂⢩⣁⠀⠀⢹⠘⣿⣾⡝⢸⡏⣿⡜⣿⣿⣿⣿⡈⣧⣿⣿⣿⠣⢇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⡿⣿⣿⣧⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣇⢻⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡍⣠⡿⣫⣽⣾⣿⣿⣿⣿⡿⣻⣿⣿⣿⢏⣾⣿⣋⣿⡿⡄⣼⣿⡇⣶⣶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣆⢀⡀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣷⣿⣯⡿⣛⢻⣩⠭⣿⣿⣏⡄⠆⢠⣶⡎⣿⣿⡇⣿⡤⣽⣿⣷⣿⣦⠙⢿⣿⣷⣦⡉⢻⣿⠀⢸⡄⢿⣿⣿⡎⣿⠸⣷⣷⣿⣿⣿⣧⣼⣿⣿⡏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢻⣷⣿⣿⣿⣿⣮⡻⣿⣿⣿⣿⢿⣿⣿⣿⣿⣧⢿⣿⡜⣿⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣫⣾⣿⣿⣿⣿⣿⣿⠿⢋⣁⣾⣿⣿⡿⣡⣿⣿⣱⣿⡿⠔⢰⣿⡏⢰⠿⣷⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣶⣄⡀⠈⠢⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⡏⣾⢋⣾⣿⣸⣝⠿⣿⠇⢰⣿⣿⣷⣿⠟⠁⣝⠳⣹⣿⣿⣿⣿⣷⣌⠻⣿⣿⣷⡀⢍⠀⢸⡇⣸⣿⣟⢧⢻⡷⣾⣿⣿⣾⣿⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢡⡻⣷⣿⣿⣿⣿⣿⣾⣝⢿⣿⡍⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣥⣾⣿⣿⣿⣿⠟⢛⣯⢂⣴⣿⣿⣿⡿⠋⣴⣿⡟⣵⣿⢟⡘⢀⣾⡏⢰⣁⣃⣘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⢁⠋⡺⣿⣿⣿⡿⢋⣡⣤⣄⠙⠛⠿⠃⣰⣆⠻⣧⠘⢻⣿⣿⣿⣿⣿⡻⣷⣌⢻⣿⣷⠡⠀⢱⣿⣿⣿⣯⡻⡇⣿⣿⣿⣿⣿⡌⣿⣿⡇⢾⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⢷⡝⣿⣿⣿⣿⣿⢻⣿⣷⣞⣻⣮⢻⣿⣿⣿⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣛⣛⣻⣿⣻⣿⣷⣾⣿⣿⣿⣿⣿⡿⠛⣠⣴⣿⣿⣿⣿⣿⣿⣟⢏⣾⣿⢟⣾⣿⢋⣾⠁⣼⡟⠁⠛⢻⣿⡿⢿⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⢸⣛⣛⣿⣿⡾⣿⣿⣿⣿⣿⣶⠄⣸⣿⣿⣦⠙⡆⡌⢻⣿⣿⣿⣿⣿⡌⢿⣸⣿⡖⠴⠀⠀⠘⢻⣿⣿⣷⣽⣿⣿⣿⣿⣿⣿⣿⠿⠇⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠱⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⡿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣻⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣁⣴⣾⣿⣿⣿⣿⣿⢯⣾⡿⣣⣿⣿⣣⣿⣿⣣⣿⠋⣾⡿⠁⠼⢇⢨⣭⣭⡁⠠⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠠⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⠇⢉⣉⣙⣛⣛⣛⣘⣿⣿⣿⣿⢛⣧⣻⠏⣿⣿⡇⢣⣘⢶⣌⢿⣿⣿⣿⣇⠘⠇⣿⣧⠀⠱⣿⣿⣧⠹⠷⠿⠿⠿⠿⠿⠿⠿⣛⣋⣁⡺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣟⣿⣿⣿⡷⠝⠳⡝⣾⣿⢻⣿⣿⣿⣿⣞⣿⣿⣿⣞⡿⣿⡇⣿⣿⣿⣿⣿⣾⡿⣛⢉⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣋⣵⣾⣿⣿⣿⣿⣿⣿⣿⣵⣿⢟⣽⣿⡿⣣⣿⡿⣳⣿⡟⣴⣿⠇⢏⣀⠻⠿⠿⠯⢥⣦⠂⠀⡄⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠈⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣷⡖⢻⠹⢿⣿⣿⣿⣿⣿⡸⣷⢌⣿⢻⣾⣿⣿⣧⠘⣯⠹⡍⣰⣶⣶⣮⣛⣡⡄⢿⠏⣌⢳⣜⢋⣽⣿⣅⣘⠃⢰⣛⠻⢿⣿⣿⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣍⣉⠩⡔⢃⣘⣿⣷⢹⣿⣯⡻⣿⣾⣿⣿⣿⣿⣿⡗⣿⣿⣿⣿⣋⣀⣘⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣡⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⣿⣿⡿⣵⣿⡟⣵⣿⡿⠰⢡⠯⣴⣤⣤⣤⣄⡀⣐⣃⣁⣄⡀⠰⣶⣦⣤⠖⠛⣂⣰⠒⠀⠄⢀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠈⠛⢦⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⢀⡀
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣧⣀⣿⣿⣿⣿⡿⢿⣄⠻⠯⣤⣟⡛⠿⢿⣷⣙⣿⣿⣮⣛⣻⢿⣿⣹⣿⡀⢸⣿⣿⣿⣄⠉⣽⠟⡓⢿⣿⣿⣿⣷⡁⣠⣿⣶⣿⡶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣬⣛⠻⠷⠮⠹⠂⠘⢿⣿⣿⣿⣿⣶⣝⡻⣿⣿⣿⣿⣿⣝⣛⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢋⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢋⣷⣿⣿⠟⣽⣿⢏⣾⣿⡿⠡⠁⠄⣀⣾⣿⣿⣯⣍⡹⠍⣛⠱⢶⣾⣦⣄⠈⣵⡄⠨⠛⠟⣿⣖⣀⣉⡛⢷⡶⢤⣤⣤⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣶⣶⣦⣤⣀⠀⠀⠈⠉⠻⠿⠿⠓⠒⠍⣁⣀''', 0.5)
def bear_art():
    echo('''⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠀⠆⠀⢄⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠛⣛⣛⢛⠻⠿⠿⣿⣿⣿⣿⣿⡿⠿⠿⠟⠛⢛⢛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⠰⣄⡘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠘⠀⠀⠉⠀⠈⠸⣤⡙⢿⣿⡿⠟⠋⣀⣠⠤⠐⣻⡟⢿⡿⡿⢿⡻⠿⣶⣮⠛⢋⣡⣴⣶⣻⣿⣿⣿⡿⣿⠻⢷⣶⣦⣭⡛⢿⣿⣿⡿⠁⠀⠀⠀⠀⠂⠀⠺⣌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡡⠉⠀⣼⣿⣿⡇⢀⢀⠈⠳⢈⢋⠔⠖⣠⣤⣰⢾⠇⢿⣿⣷⣴⣶⠶⣭⡀⡈⠋⠉⢩⡄⣀⣨⡥⢶⣤⣤⣼⣿⡇⠶⡦⣬⣿⡿⢶⣌⢋⠐⠃⣀⣶⠰⣾⣿⣦⠀⠻⣦⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢩⡀⢸⣿⣿⣿⣿⣿⡾⢃⣴⣿⡇⣴⣾⣿⣭⡹⣹⣿⣿⣿⣿⣿⣿⠞⣄⣈⠰⠀⠴⠙⠀⠘⣀⣦⣿⣿⣿⣿⣿⣿⣿⣷⣯⣭⢻⣾⣿⣿⣷⡄⠿⣿⣿⣿⣼⣿⡆⠀⢘⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠘⡃⠘⢿⣿⣿⡿⠟⣱⣿⣿⣿⣷⣿⣟⣱⣶⡍⢻⣿⣿⣜⣿⠿⠻⠗⠀⠀⠀⠀⠀⠀⠐⠤⢄⡐⠻⡻⢿⣿⣿⣿⣧⠛⣿⣿⢻⣿⣿⣿⣿⣿⣧⡙⣿⣿⣿⣿⠇⠀⢖⠂⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠃⠀⢐⣿⣿⢋⡼⣿⣿⣿⣿⣿⣿⠻⣿⣿⠰⠤⠅⠛⠳⠈⠀⠀⣀⣤⠦⠦⠀⣤⡄⠘⢶⣶⣬⡳⣄⠈⠹⠟⠋⠁⡴⢿⣿⣷⠝⣟⣿⣿⣿⣿⣷⡘⢿⣿⠇⠀⠠⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠘⣻⠿⢉⣾⣿⣿⣿⣿⣿⣿⣿⡧⠀⠀⠀⠀⠄⠀⢀⣴⣾⣐⡃⠀⠀⠀⠀⣿⡷⠀⠀⠀⠀⣱⠈⣷⣄⠀⠀⠀⠀⠘⠀⠠⢺⣿⣿⣿⣿⣿⣿⣿⣌⢻⡷⡠⠌⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡉⣤⣿⣿⣿⣿⣷⢹⣿⣿⣿⣿⣳⣦⣤⣤⣤⣆⣾⣿⣹⣿⣷⣦⡄⢀⣴⣿⣿⡀⠀⣤⣶⡞⣰⢿⣿⣖⣤⣤⣤⣤⣤⣴⣿⣿⣿⣿⣿⣿⣿⣻⣿⣦⠘⣣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠘⠩⡟⡏⢸⣿⣾⣿⡻⣿⣿⣿⠹⣿⣿⣯⣿⣿⣿⣿⣍⡊⠛⠁⣺⣿⣿⣿⣷⠀⠈⠏⢀⣵⢿⣿⣿⡌⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⡷⠸⣿⣦⠉⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⡄⠐⣸⣷⣜⠂⠻⣿⣯⣷⠮⣻⣿⣯⢪⠻⣿⣿⣿⣿⣿⣯⡟⠋⣴⣿⡿⣀⠈⢿⣷⡄⢿⣿⣿⣾⣿⣿⣿⣿⢟⣿⣿⡿⠋⢴⣿⣿⡏⠁⢚⠹⡷⠐⠸⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠈⢐⠚⠮⢭⠿⡇⢠⡈⢙⠿⢿⣮⣹⣿⣧⡑⢼⠟⣿⣿⣿⣿⣿⠂⠻⠿⠐⠛⠛⠐⠿⠰⢸⣿⣿⣿⣿⣿⣿⡗⣹⣿⢟⣡⣾⡿⠟⠉⠀⢶⣿⣾⣩⠄⠙⠻⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⡀⠘⠦⠄⠒⠀⣄⢷⣆⠛⠲⢭⡳⣿⡻⠦⣝⡙⡂⡀⣿⣿⣿⣿⣥⣄⢀⠀⣈⢠⣉⡀⠰⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣷⡿⠋⡝⢢⣥⠾⣿⣿⠟⣁⠐⢉⡁⠖⢋⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡸⠁⡶⠾⠄⡁⣂⡉⢙⡿⣿⡮⣧⣻⠦⢩⣝⠖⣄⠑⠀⣻⣿⠿⠿⠋⢷⠶⠾⠟⣘⡛⠿⠶⠶⡈⠛⠿⢿⣿⣿⣿⢏⣿⠟⣉⣡⡾⣫⣶⣾⣿⠗⠋⠁⠀⠒⣬⠤⠍⢿⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⡇⠀⣯⢘⡻⣿⣛⡻⡳⣍⡒⡿⢿⣝⢿⣷⣏⢙⠆⡀⠀⠈⢠⣶⣿⠃⠚⠛⠉⠉⠉⠉⠉⠛⠛⠆⢸⣷⣦⢉⠛⣿⣶⣶⢏⣽⣯⣾⣿⠿⠉⢚⣵⠿⠉⢽⡿⠦⣭⡂⢸⡆⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⣬⠇⣌⣶⣶⣆⣍⣿⣦⣙⣮⣛⣷⣿⣿⣾⣇⠸⢂⣥⣾⠀⠀⢸⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⢀⣿⣿⣧⢾⣞⡿⡿⢗⣶⠾⣋⢔⣵⣿⣟⡢⣭⣭⡇⠈⣻⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣸⢡⡾⣿⣼⣿⣿⣿⡉⠄⢘⡷⢏⣿⣿⣿⣏⣱⣇⣹⣿⠏⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠀⢰⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⠿⠋⠭⠿⣻⣿⣏⣡⡤⡘⣇⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠬⡘⣿⡬⣷⡏⠵⠖⠉⢿⣿⣝⣿⣿⣿⣿⣼⣿⣿⣿⣿⡇⡇⢸⡞⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠟⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡞⣁⣾⠛⢫⣭⣽⣬⡝⣰⠁⢟⠃⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠰⠂⣓⠙⣿⣑⣶⣶⣟⣛⡿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡃⡇⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⣛⠺⢆⣲⣒⣶⣾⡏⣳⠇⡐⢣⡅⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣴⠞⠓⢰⣟⣥⣸⣿⠟⣛⣿⣿⣿⣿⣷⣿⡶⣻⣥⣿⣿⣿⡧⠁⣸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠘⣿⣿⣿⣿⣿⣟⠦⡹⣷⣟⣋⣒⣒⡚⢿⣿⣏⣉⡛⡆⢿⡢⣽⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡐⢈⣖⣶⡎⣿⣿⣷⣶⣾⣿⣿⢟⣫⣥⣼⡿⠚⣽⣿⣿⣿⣿⡇⠐⣿⡇⠈⣅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡁⢸⣿⡇⢸⣿⣿⢻⣿⣮⡷⠮⣤⣂⣑⠭⣿⢿⣿⡖⣶⣾⣇⣷⣄⡪⣂⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⡇⢻⣿⣫⣧⢹⡿⢿⡟⣿⣯⡿⡿⣫⢝⡃⣨⣾⣿⢟⣽⣽⣿⣏⠀⣿⠇⠀⡟⠀⠀⠀⠠⢤⣀⣤⠄⠀⠀⠀⢹⠁⠿⣿⠁⣾⣿⣯⣼⡻⣿⣿⡕⢂⡪⡙⢿⢈⣚⡛⢿⡿⣶⡍⣬⡛⢾⣞⠠⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣦⠃⢸⢏⡀⣻⠈⣷⡵⠟⠿⢛⣆⡐⠩⣊⣾⣬⣷⣺⣿⠿⢟⣿⠇⠀⠂⠀⠀⢶⠀⠀⢔⣳⠚⠿⠗⣘⣀⠀⠀⣶⠀⠐⡇⡄⢹⣿⡛⡿⣿⣗⣲⢁⢳⡽⢌⡂⣠⡹⢶⡷⣜⡢⢙⡚⢨⣷⡂⢿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⠷⠆⢸⢸⡟⣻⣄⣨⢦⣴⣿⣶⣿⣶⢚⣿⣿⣋⣸⣿⣷⣽⢿⣿⠀⢸⠇⢀⣆⣶⠀⢀⣿⠀⠀⠀⠀⠁⣿⡁⠀⢰⢠⡆⢰⣷⢨⣿⣏⣍⡒⣻⣃⣘⣛⣒⢓⣮⣿⢅⣶⣦⠪⡉⢤⣿⢾⡇⠁⢰⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⢿⣢⢸⡌⣿⡿⠟⡀⢿⣿⣿⣿⠟⣿⡿⠉⢷⣿⣿⠹⣯⣽⣽⣟⠀⢀⡄⢸⣿⡌⡄⣄⣀⣤⠀⠀⠀⣠⡈⠀⠀⡦⣾⡇⣿⡇⢸⢿⣿⣷⣼⠏⣿⣿⡿⠋⢴⣿⢣⣾⣿⣿⠷⠩⠷⣴⣬⠁⠀⡸⣿⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢼⣾⣿⢻⢧⢹⣟⣿⣿⣎⣿⣯⣻⣭⡝⣿⠇⣉⠞⢫⣄⣨⠍⠟⣵⠀⠈⣷⢸⣿⣧⠁⠙⣷⣿⣿⣿⣿⣻⣷⠋⠀⢺⣿⡇⣿⠏⢸⣯⡢⠝⠃⠐⡚⠧⠄⢰⣍⣃⣑⣙⣿⡿⠀⣮⣕⠾⡏⠘⠐⣻⣾⣷⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢠⡘⢽⣱⣿⢸⣈⡛⠹⡾⢎⣉⣿⣿⣿⣿⡿⡿⠯⠄⢉⡈⠵⣸⣿⣷⠀⠐⣿⡎⣿⣿⣤⣄⠀⠘⣛⣿⣟⡋⠀⢀⣤⣼⣿⢇⣿⠀⢸⣿⣻⡆⢠⢑⡙⠲⠼⣷⣦⣾⡿⣿⣮⠁⢠⣍⢍⣿⠀⡆⣴⡌⣟⠏⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡗⣸⣿⣿⣇⠃⣠⣾⣿⣿⡯⠉⣿⣿⠍⢀⡁⣿⡿⠉⣴⠞⣼⣿⣿⠂⠀⣿⡷⣬⣍⠿⢿⣿⡗⣶⡄⣴⡶⣿⣿⠿⠏⠍⠸⣿⠀⢸⣿⣿⣇⠲⣆⢙⢿⡧⣀⠦⢹⣿⣮⠉⢼⡓⣶⣦⡉⠀⣼⣻⠳⣎⠂⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢘⢿⣿⣽⣿⣿⡇⢀⢻⣿⣿⡟⠃⣩⡿⣿⣿⢣⣾⢔⡌⣡⡿⢫⡵⠧⢃⠀⢹⡇⢘⠛⣿⠷⠾⠶⣭⣶⣭⣼⠔⠰⣿⡏⡂⢸⡟⠀⠘⠮⣤⡙⣷⡜⣀⠡⣶⡟⣿⡾⣟⠐⢄⢿⣷⢻⡏⠀⣼⣿⣿⣁⣿⡆⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣼⢸⣿⡏⣿⣿⣷⣮⢁⡙⣯⣾⡿⢛⡤⠛⢱⣿⢋⣌⣼⣿⣼⣿⠟⢰⣽⠇⠀⢿⡆⢣⡟⡅⣿⡏⣿⣿⣿⢈⣿⠀⢿⡏⢡⣾⠁⠠⣿⣧⢿⣿⣊⣽⣌⣳⡹⣷⠈⠃⣄⠲⢬⣮⡛⠊⢀⣔⢽⣿⣿⣿⣿⣷⡆⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⡔⣧⣾⣿⣿⣾⣿⣯⣷⣼⡃⠉⠙⢫⣾⣿⣷⡈⢹⢏⣼⢟⣽⣿⣟⣨⡯⢷⡅⠐⡈⢿⡌⢳⣿⢰⣿⣻⣿⡟⣿⡇⣿⠜⣡⡾⠃⡄⣼⣾⣿⡃⣿⣿⣿⣿⣍⠻⠈⢠⣾⣿⣾⣷⠮⠁⢰⣶⢯⣚⠿⢿⣿⣿⣎⢻⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⡎⡆⣿⣿⣿⣿⣆⣿⣿⣿⣯⣶⡄⢹⠿⣿⣋⣶⣶⣆⠈⢋⡼⣿⣿⣿⠋⣰⡟⢦⣧⠁⠠⡙⠀⠉⠀⠿⣶⠻⣂⠛⠁⢈⠀⠛⠀⠈⣼⢹⠛⣇⢹⣿⣿⡿⠟⠛⠀⡰⣾⣯⢛⠛⠀⠀⢠⣌⡛⠓⡝⣃⢸⢿⣿⣷⡗⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢫⠎⣠⣿⣿⡟⢹⣿⣿⠃⢿⣛⣿⠟⣫⡦⠈⣷⣎⣛⢛⠁⣐⣡⠆⠛⠿⢫⣾⢯⢣⡴⢏⠄⠁⢹⣦⡀⠀⠈⠛⠛⠛⠁⠀⠀⡀⠊⢀⣬⣽⣼⣸⣿⣦⡻⠏⠁⢰⣜⠂⢝⠛⡛⠀⠈⠀⣄⡛⠿⣓⡸⡏⢺⣿⣿⡟⣿⣇⠻⣿⣌⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣰⠚⢂⣬⣿⣾⣿⣸⣿⠇⣅⣛⣵⠖⣨⣾⣿⢟⡈⢻⣿⠉⡾⢋⣵⣶⣟⠀⢠⠙⠀⣼⢁⠄⣷⣆⠀⡙⠻⣗⣀⣀⢁⢁⠀⡀⠸⢋⣠⣰⣾⢾⡟⣇⠁⠃⡀⢤⣲⡶⢝⠳⠎⠁⡢⠀⣀⢾⣷⣤⠒⠮⣙⢶⡑⢽⣿⡓⣿⣿⣧⠈⣿⣷⣙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣡⡾⢀⣴⣾⣿⣿⣿⣿⠛⣿⣿⣾⣿⣭⣶⣻⣿⣩⣄⣽⡿⢠⡙⠢⠀⢈⡞⡿⢣⣰⠏⢀⠈⡵⠟⠼⣧⢡⣢⡇⣿⡶⢀⢠⡭⡄⠀⣶⣿⣼⣹⣿⡹⠆⠳⡀⠀⡀⢹⡄⡹⣷⠂⢀⠀⠀⢀⡐⢿⣃⢬⣻⡓⠶⢬⢙⣛⢦⣃⠹⣿⣿⣿⣼⢦⣬⠻⣷⣯⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⣠⣴⣶⣶⣿⣿⣿⣿⣿⣿⣦⣸⣿⣏⣹⣿⣿⣿⣿⣧⣼⣿⣧⠬⢱⠂⣤⣘⢣⠀⠿⢁⣤⠎⢠⡴⠇⠀⣣⡀⠟⡵⠌⡜⣰⣤⡗⡄⣌⢎⠳⣝⠷⢀⡙⠀⢰⣤⡸⢡⣜⠿⠣⠡⠈⣀⠄⠳⡉⢀⣾⣿⣆⣿⡇⢹⣿⣮⠙⠿⣿⢁⣽⣿⣿⣿⣿⣿⣧⣠⣽⣿⣮⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⠐⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⣼⡿⢟⣕⠀⠀⣠⡏⠋⠀⠊⣰⣟⠉⣴⠟⠁⣠⠖⡈⡀⠀⣁⠀⢼⡿⠈⡧⢡⣿⠈⢠⢋⠀⠀⠁⢢⡘⢛⢷⡄⢗⠆⡀⠠⠀⠋⣤⡐⠳⢶⣝⢿⣋⣡⣬⣾⣿⠿⢸⣷⠎⣾⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⢿⣦⣙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⢐⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢿⣿⣿⠟⣿⣿⠟⣵⡟⡁⡀⣶⡿⠁⠀⢀⣾⣿⡏⣨⡇⢂⣴⠋⡆⠁⠕⠈⠹⠀⡘⡇⠄⠁⠸⣹⠀⠰⡌⠁⢦⠀⡆⢻⣀⠃⢋⠈⣶⣵⣀⠀⠁⠻⢧⡢⡀⢝⢷⡼⣿⣿⡿⣯⣤⣽⠟⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣻⢿⣷⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡉⠂⣶⣼⣾⣿⣿⣿⣿⣿⢟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⠱⣷⣧⣿⢏⢾⣉⣞⡱⢡⡅⠆⣴⣆⣿⠝⠀⢈⠉⠐⣉⣼⠖⣡⠀⡄⠀⣰⡏⠇⠓⠰⠀⠐⠃⢼⣶⡈⠀⣄⢄⡽⢾⡬⢐⠈⠁⠀⠐⢬⣇⣴⡔⢦⢹⠸⡘⠎⢻⢎⢿⡇⢮⡏⢈⣰⣿⣿⣿⣏⣿⣿⣿⣿⣮⡻⣿⣿⣿⣿⣿⣦⡹⠻⣷⣝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠂⣤⣶⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡿⢿⢻⣦⡼⠿⣫⡔⣿⡏⣼⡟⠻⢣⠀⢀⠁⡶⠀⠘⠃⠚⡏⡿⠀⣴⡿⡠⠂⡿⣰⣿⠘⣧⢰⡝⣷⡀⣽⣧⡙⠀⠙⠂⠀⠀⢂⠈⠢⡻⣯⣏⡈⣿⡇⣮⡻⣿⢊⣶⡟⠘⢣⣼⢿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣷⣦⣽⢿⣿⣿⣿⣿⣶⣌⡛⣷⣍⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡡⠊⣺⣿⡿⢿⣿⣽⣿⣿⣽⣿⣿⣿⣿⡿⠿⣟⣯⣿⣿⣿⣿⣿⢫⣿⣿⣷⡈⢸⣿⣧⢺⡋⣰⣯⣾⡿⣁⣤⠆⣰⣾⠒⠀⠀⠀⢧⡆⡇⣾⣧⠉⣿⡿⠃⣠⡏⠿⣷⠹⡿⢿⡆⣆⢿⡎⠉⠀⠀⠀⠀⢀⣂⣦⡒⢷⣍⠻⣿⣬⣟⢈⣻⢶⣿⡷⠄⣡⣿⣿⣏⢿⣿⣿⡶⣭⣻⠿⣿⣿⣿⣿⣟⠷⣝⡻⣿⣿⣿⣿⣿⡾⡿⣷⣯⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡡⠊⣠⣾⢟⣩⣾⣿⣿⣿⣛⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⢻⣯⡿⣿⢈⡻⣷⣏⣧⡇⢋⣴⣾⣿⢁⣺⡿⢡⠀⣰⣽⠃⠂⠀⢠⠁⠈⢼⢋⡆⠀⢿⡇⠛⣷⠖⠙⣮⢹⡏⠆⢀⠀⠀⠀⢳⣄⠀⢿⡻⣧⣦⢻⣿⣾⣍⢯⢳⣿⢏⠿⠁⢰⡿⣏⢿⣻⣮⣿⣿⣿⣝⡻⣿⣷⣶⣾⣍⢙⢧⡺⣿⡘⣿⣿⣿⣾⣽⡿⡦⠹⣿⣌⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣈⣡⣼⣻⢿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣫⣿⣿⢟⣿⣿⡟⡿⣽⣿⣿⢿⣿⢷⢫⣿⡴⢋⡴⢣⠈⢿⡟⢡⣿⣿⡿⣱⡞⣈⣴⡡⣠⡾⠟⠀⢀⠆⠉⠀⢸⠈⠸⠁⡞⠰⣆⢀⣶⠘⠆⠙⠀⠑⠀⠈⣴⢆⠈⠊⠿⢆⠲⣱⡝⡟⣇⡿⣿⣿⣦⢻⣿⠇⢠⣷⡘⣷⡸⡎⢧⢿⡟⣿⣿⣷⢻⡻⣿⣿⡿⢿⣧⡙⢷⣬⣿⣿⣿⣿⣿⣽⢿⣿⣚⠪⢻⣷⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⡄⢁⣡⣼⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣵⣿⢿⢋⣵⣾⣿⡿⢣⡎⠤⢠⣿⣟⣴⡟⢐⣤⣶⠂⠀⢾⣿⡟⡇⣴⠃⠻⣛⣼⣿⠏⠀⡰⢋⡞⢀⠤⠘⡄⠀⠀⠶⠆⡛⠛⣋⠰⠂⠀⠀⠠⠀⢠⠘⣧⠱⡘⢾⣷⣷⣝⡿⢇⢳⡁⢻⣿⠿⠄⠀⢸⣅⡛⡟⣮⣻⣿⣌⢾⣿⣎⢿⣿⣷⣦⠛⢿⣿⡪⣹⠟⢾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⡻⣎⠻⣿⣮⡛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⢀⢈⣥⡶⣟⣩⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠑⣡⣟⣿⣡⠦⢋⠿⣋⣼⣵⠫⠀⢠⣿⣿⢟⢉⣴⣿⣿⣷⣾⡆⡧⢂⠈⠥⢫⡼⠸⠟⢉⡘⢀⣾⣰⣟⠀⠀⣤⡸⠀⠄⠰⢰⣘⠹⡿⢈⣰⢰⠀⠆⡶⣰⡌⠀⢘⣷⣙⡘⠟⣛⠙⢿⠸⣌⠇⠜⠀⠀⣁⣾⣼⣿⣿⣦⡙⣿⣿⣿⡎⢏⢿⢇⢻⡙⣯⣒⠎⣞⣿⡻⣯⢮⠻⡻⢿⣿⣿⣿⣽⣿⣿⣿⣟⣛⠮⣌⡛⠿⣮⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣋⠂⣴⣾⣗⣫⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣠⡾⣹⣿⣿⣧⢒⠟⣥⣿⠫⠀⣠⣴⣿⠟⣐⣋⣼⣿⡿⢏⣾⣿⠟⣡⣸⠀⢀⠈⠁⢸⠀⠎⠐⢸⣿⠗⣹⡀⠘⣿⡟⠀⠐⠃⣧⢟⣤⠗⠸⠅⡏⠀⠀⠐⣿⡕⢠⣾⡟⢿⣿⠸⠝⢇⠻⠀⠀⠀⠀⢼⢀⠻⣿⣿⡝⣿⣿⣧⡘⣿⡹⣿⣦⡑⢼⣌⢟⢭⡲⣆⢜⣿⣿⣯⢳⡝⢿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⡾⣿⡺⢅⣻⡻⣧⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠅⡆⣠⣶⣶⣶⣯⣟⡿⣿⠿⣿⣿⢿⣿⣿⣿⣿⣟⣴⣟⣫⣾⣿⣿⡿⢁⣢⡾⢓⡡⣠⣾⣿⡿⢣⣾⠟⣹⣿⢟⣴⡿⣋⠀⣼⣻⢋⣴⡺⠀⠃⠀⠠⠀⢠⢿⡇⠀⢿⣇⠀⡻⠇⢰⠄⠄⢁⣆⠠⣠⢈⡀⠀⠀⣼⠀⡿⡁⢸⣿⠇⠢⣿⢇⠠⠐⠀⠀⠀⢸⣿⡜⢿⠳⠹⣿⢻⣾⡛⣿⣧⠻⣷⡝⢿⣟⣶⣀⢰⡪⣷⡘⠎⢿⣿⣿⢧⣝⢿⣎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⠿⢓⣤⣈⣉⠻⣦⣝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢋⠡⠤⣂⣡⣤⣿⣾⣿⣟⣻⣿⡿⣿⣿⣿⣥⣭⣿⣯⣭⣍⣲⣾⣟⣛⣽⣿⡿⢢⡿⠉⢠⣾⡿⣫⡿⡿⢁⡿⢫⣾⣿⣥⢛⣋⡔⣡⣞⠻⣱⣿⠟⣣⡤⣠⠀⠀⠀⠸⠟⠁⢀⠸⠇⠀⣹⡆⠸⡇⢰⣾⡍⣦⢥⣌⣷⣶⢠⡶⠂⢾⡁⠘⠿⠁⢀⡇⠋⠀⠀⢀⣠⠠⣅⡻⣿⣦⠳⣷⣌⠳⣝⣓⣘⣻⣷⣜⢿⡎⢿⣿⣌⢷⡻⡔⢬⡳⡄⢿⣿⣿⠻⠟⠨⣭⢿⣛⣛⣿⣓⣙⣿⣟⣿⣷⣾⣿⣿⣿⣯⣷⡈⠻⣿⣾⣝⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⡉⣥⡴⢠⣋⠴⣻⣿⣛⣃⠒⠙⠻⣿⣿⣛⣾⣿⣉⣿⣿⣿⣿⣿⣟⡿⢟⣛⠛⢉⣉⣩⠞⢛⣴⣾⠟⣋⣴⡿⢋⣶⣿⢅⣽⣻⢟⣿⢫⢖⣼⣛⢍⣴⣟⢛⣨⣶⢞⠛⠈⣀⠀⠄⠈⠀⡾⢘⡃⠀⣿⡇⠓⠲⢦⡛⢫⣰⣶⡺⠛⣤⣼⠃⢋⣾⠇⠀⢐⠀⡎⠀⠀⠀⢨⡈⡟⢿⢶⣝⠒⣋⢠⡸⣿⢷⡺⠉⢻⡛⣝⢯⡁⣿⣦⡕⢿⣧⢛⢻⣤⣇⣿⡮⣙⠁⠘⣝⠳⢾⣛⠻⢶⣿⣿⣿⣿⠛⢿⣿⣿⣿⣿⣿⢿⣧⣼⣯⣄⠪⣝⠻⢶⣮⣙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⢡⢠⢼⣁⣶⠧⣚⣉⣸⣾⣿⣯⢻⣿⣿⣶⣥⣍⡯⢭⣿⣾⣿⣳⣿⣟⣻⣿⣭⣵⣿⣿⣿⡯⢠⣶⡯⡶⢀⠎⣽⠟⣫⣼⡿⢡⣾⣿⣵⡏⠊⣠⣿⡟⡃⢨⢴⣶⣾⡿⣣⣢⢏⣾⣥⣾⡶⣀⠀⢀⠀⢲⡆⣌⡉⠀⡔⣿⠀⢀⣿⣿⣦⠘⣹⡷⡄⣹⣅⠀⣶⠀⠀⠀⣀⢰⣼⣮⣻⣎⣆⢮⠿⣿⡐⣦⣉⢪⡳⣷⡄⢙⢯⣎⢳⣍⢌⢿⣯⣘⢿⣦⢳⡌⢽⣽⣶⣾⣿⣿⣶⣮⣝⡲⢭⣼⣿⣿⣯⣿⣿⣶⣿⣿⠿⣛⣦⣽⣷⡶⠒⠿⠯⠎⠃⣶⣍⠛⠿⣶⣭⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⣡⠐⡀⣈⡤⢫⣶⣶⣿⠍⢽⣿⣿⣿⣿⣶⣶⣭⣝⡛⠿⣿⣿⣿⡽⠏⢩⣶⣭⣤⡿⢿⠟⣡⣾⣯⣶⡟⢻⣿⡇⢠⡼⠫⢠⣿⠋⣰⣿⢿⣿⠋⠐⡽⠟⡡⢪⠖⣵⡿⡿⢡⣼⡟⢱⠿⣹⣿⣷⣿⣿⡄⠀⠸⣎⡑⠈⠀⠆⠃⣿⣀⢿⢻⣟⢻⢀⣽⡜⢠⠁⠀⠀⡁⠐⠀⢄⣿⡧⠦⣝⢿⠻⣌⠁⣥⠉⢻⢺⣮⡳⣝⢿⡛⢮⡢⣻⢧⡻⣷⣆⠿⣷⡜⣿⣯⡙⢾⣿⣿⢿⣮⡻⣿⣝⢿⣿⣿⡋⢻⣯⡻⣿⡿⠿⢯⣷⣽⣿⠿⢟⣛⣬⣽⣿⣿⣷⣿⣿⣶⣅⡀⠂⠙⢿⣷⣭⡻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⢑⠒⡋⣡⡴⣺⡿⠞⣡⣿⣯⣥⣿⣿⣿⣯⣯⣝⣿⣿⣿⡶⢉⣷⣦⣦⢔⣯⣬⡟⣿⣿⠟⠻⣁⣴⣶⣾⣿⣿⣯⣽⠖⢠⣼⠂⣷⣿⣭⢰⣹⠃⣿⣿⠇⠀⠀⢈⣦⡉⢺⡏⠃⣁⣤⣽⠆⡠⣾⠿⡿⢿⢛⣥⣾⣿⡾⣏⢳⣏⠈⠀⠉⢿⡏⢃⣾⣿⠠⠋⣿⠁⠃⠀⡘⣧⢁⢸⣾⣷⣬⡻⢿⠏⠈⠗⢌⠂⣮⣧⣐⣁⢿⣷⠾⠂⠉⣀⠠⡸⣷⣷⠞⣯⣆⢹⣷⡈⡿⣿⣮⣿⣿⣿⣿⣿⣿⣯⣤⡿⣿⣟⣽⣿⢿⣾⠿⠿⢿⣯⣿⣾⣿⣿⣿⣿⡿⢾⣶⣾⣿⣿⡿⣿⣿⡷⢌⡑⠍⠉⠛⢷⣯⣙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠅⠰⠞⠠⣄⣭⣿⡿⢋⢰⣵⣾⣿⣻⣿⣿⣿⣵⣶⣾⣿⣿⣟⡋⢴⡿⠟⢡⣄⠀⣭⣬⠴⢆⣴⣶⣿⣹⣿⣿⣿⣟⣼⡿⣦⣼⣿⠋⡀⣿⣯⠏⡆⣯⣾⣿⢁⡴⢿⠡⢺⠟⣿⠋⠈⣼⣿⡟⠋⣶⣾⢟⡾⣡⠡⣾⠛⢋⣽⢶⢟⣨⡿⣧⡄⡔⣿⠀⠀⣿⢫⠀⠀⢹⡆⡄⣶⣿⣇⡹⢷⣯⡉⢓⠖⡀⣠⡳⡸⠷⡴⡝⠻⣿⣿⠰⢛⢿⠱⣤⢿⣿⣮⡹⣿⡷⡹⣿⡜⡿⣿⣔⠙⣿⣿⣿⣿⣿⣿⣾⣿⣿⡿⣶⣶⣬⢽⣭⣙⠋⠉⣉⠹⣿⣿⣿⣿⣿⣿⣻⣿⣭⢛⣿⣿⣿⣿⣿⣯⡓⠙⢷⣍⢈⠀⢎⡻⣷⣮⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⣀⣠⣜⠺⠒⢚⡿⣿⡟⠑⣠⢏⣿⢟⣵⣿⣯⣵⣿⣿⣿⣯⣽⢭⣽⣿⠍⣳⣷⠟⢁⣴⠟⣡⣾⣿⣿⣾⠟⠻⢿⢛⣽⣿⠿⣞⣽⣿⡕⣼⣧⣤⠋⢸⣿⢏⠞⣵⢯⢟⠉⢀⣣⠦⡟⢄⡆⣿⣫⣾⢸⣿⣭⢏⣼⣽⠯⢨⢴⡿⣃⡴⣿⠿⣡⡭⢛⣷⣿⠀⠸⣿⢸⠟⠀⢼⣽⠏⠮⣧⡻⣿⡦⣙⡻⣷⣝⢿⣿⣷⡔⣯⣿⣇⢿⣝⢋⠘⡸⢸⣇⣮⠂⠹⣶⡄⣌⠳⡝⣧⣱⢹⣿⣿⣷⣿⣏⣝⣯⣽⣿⣿⡿⠿⣿⠿⡿⣽⣷⣦⣙⢷⣄⠙⢿⣜⣿⢿⣿⣟⣻⣿⣿⣯⣿⣿⣿⣿⣧⡻⢿⣷⣧⡠⣝⢷⡘⠄⢄⣉⡉⡻⠷⣭⡛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⠁⠀⠠⠖⢘⣩⡀⠀⣸⠿⠟⢣⣾⣾⠟⣡⣾⡿⣾⣿⣿⣿⣿⣿⣿⣿⣿⢇⣻⡿⠅⠐⣀⣅⣴⠟⣁⣴⣿⣿⣺⠟⢩⣤⣿⣿⡿⣋⣥⣶⠿⣋⣯⣾⣽⣿⣿⡆⣼⠏⢂⢞⡇⢨⠂⢄⡿⣣⢠⢀⣿⢣⠇⠟⢩⠛⠛⡅⢸⣭⡶⢀⡫⢩⣾⢫⢎⢄⣼⣿⣿⣿⠟⠁⠥⢆⠛⢘⢒⠤⣅⠺⣿⣿⣿⣷⡝⡜⣎⢷⣎⢉⣃⢯⣉⣟⠈⡙⡟⣘⢿⡌⣦⢷⡀⡿⢜⢶⡀⡹⣟⠘⡲⡜⠜⡇⢠⣿⣿⣿⣻⣙⡻⣿⣥⣝⡻⢷⣦⣴⣆⣃⣿⡿⣿⡯⣂⠙⠷⢄⢙⣣⣬⣛⣿⠿⢿⣿⣯⣽⣟⣿⣟⣿⣿⣖⢿⣯⠹⣮⣜⢿⠸⣦⣄⠀⡒⠐⠾⢽⣶⣪⣍⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠠⠆⣂⣘⠩⠐⠂⣉⣡⡖⣢⣴⡶⢆⣸⡿⢡⣿⣿⢯⣾⣿⡿⢻⣿⣿⣿⠟⢩⣴⣿⡿⢗⣤⣾⣿⡟⣡⣾⣿⣿⠟⢉⡅⣠⣾⣿⢛⣯⣶⣿⠿⠇⣻⣿⣿⣿⣻⣿⡿⢃⡌⢰⣼⠟⢠⡌⡄⠘⡴⠅⢁⣼⣿⠏⠀⣞⡿⣶⢢⣿⠩⠋⢰⣿⢰⣿⠧⢫⢎⣼⣿⢟⣫⣵⢎⣔⡿⣋⢠⣮⢹⠻⣶⡌⣮⣑⡶⣿⣷⡘⣜⠎⣿⡆⣿⡇⠈⢧⢳⣆⢿⢹⣰⡅⠸⣾⣧⠸⣾⣧⠱⢵⣸⡄⠿⡄⠀⢡⡸⣿⣿⠟⣨⣾⣿⣿⣾⣿⣧⣬⣿⣿⣿⣿⣝⢝⠻⣿⣮⣿⣦⡻⣮⢻⣧⡻⢿⣿⣾⡝⣿⢿⣿⣿⣿⡿⣿⢿⣮⢿⣧⣮⡻⣮⠳⣶⣭⣕⢤⣙⡳⠦⠍⡉⠿⢿⣶⣭⣛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠟⣩⠀⣀⣁⠰⢛⠩⠶⠚⣉⣬⠟⢋⡀⣵⣿⣿⣯⡼⢁⠄⣾⣿⣿⣿⢋⣤⣾⡿⣿⠋⢶⡟⠛⣋⣴⡿⠟⠛⣉⣬⣿⡿⠛⢫⢆⡟⣼⣿⡟⣡⣿⠿⠛⣧⣦⣾⣿⣿⣿⣿⣿⡟⣱⡿⢐⠄⠇⢠⣾⡗⣀⣶⡇⢃⣮⣷⠇⡄⣼⣟⡇⢃⣟⠵⠁⣱⠿⡁⢛⢫⡶⣫⡞⣛⡏⣼⡿⠃⣪⡵⠨⢀⣿⣿⡀⢭⣪⣭⡲⣿⣷⠸⣟⢻⣌⣷⡝⢃⠌⠿⣦⠉⠧⣻⡎⠜⣿⣧⠠⠹⣿⣷⡘⣭⣴⡸⣿⣷⡜⠇⢀⣺⣿⣿⣿⣯⡿⣿⣿⣿⣽⣿⣿⣿⣿⣟⣿⣿⣿⣎⢷⢨⠻⣿⣿⣽⣿⠻⣿⣿⣦⠙⢿⣿⣥⣄⢻⡟⣧⡅⠨⢷⣟⢦⣿⣍⢃⠹⣀⣶⣭⣟⣻⠜⠯⣑⠄⠬⢥⣒⠦⣭⡛⠷⣮⣟⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⠟⠋⣴⣺⣵⣿⣟⣥⡼⢛⣤⡾⠛⡉⣠⠶⣋⣤⣾⣿⡿⠛⠴⠎⡄⠉⣯⣿⣷⡾⠟⣿⠊⣑⣠⡋⣰⡽⢟⣩⣤⣶⣿⣿⣿⠟⣡⣾⣇⡏⠐⠟⣫⣾⣿⣠⣶⣿⣿⠿⣛⡻⠿⢿⡿⣿⡇⠋⡁⣪⠂⠐⢠⡇⢇⣿⢩⢃⢨⣽⠏⠐⣱⠿⠟⣸⠻⠧⣰⡾⡵⠫⣡⣴⣿⣸⣯⢠⡭⣺⢏⠀⣴⢏⣾⡆⣿⣿⣯⢿⡈⣿⠽⣯⠉⡸⣷⣨⣥⣽⣷⡹⣦⣶⣟⢮⡁⣄⢨⡗⢠⠹⣿⣷⢣⢻⣷⣅⡻⣿⣿⡘⣏⡁⣆⢻⣿⡜⠛⢞⣿⣿⣿⢿⣿⢿⣿⣿⣿⣼⣯⣵⣬⡻⣿⡎⣧⢱⣽⡻⣿⣿⣷⣦⣍⣛⠻⣷⣆⣸⣿⠓⠝⢚⣿⢧⣆⣹⣿⣿⠟⠈⢷⡹⣿⣿⡻⣮⡝⢦⣈⠑⠲⣤⣝⠧⣤⡁⠷⣜⣟⠷⣬⡛⢿⣿⣿⣿⣿
⣫⣥⣬⣾⣿⣿⣿⣷⡿⠋⣽⡿⣫⣔⡜⣹⠋⣴⣿⣟⣫⣾⣥⣴⣶⢸⣁⢸⣿⣇⣯⡴⠖⣡⣾⡿⠋⣴⡿⣃⣾⣿⣿⣿⠿⠋⣤⣾⡿⠟⠉⢀⣡⣴⣿⠿⣛⣋⣭⣵⣾⣿⣿⣿⣿⣶⠀⢽⢻⣄⣡⡟⣰⣴⠘⠃⢸⣿⡌⣾⣿⢃⡄⣠⢯⠟⡀⠁⣵⡆⡉⣨⣴⢋⣻⣿⣿⡍⣿⣏⣾⢁⢃⡄⣣⣿⠟⣼⡿⣸⣯⠸⣿⡹⣿⡈⢲⣽⣾⢿⣿⡟⠣⣿⣿⡻⡝⠇⠑⠠⠰⣯⠀⠀⢻⣌⠌⢰⡝⣿⢹⢸⢿⡇⢸⠇⣯⢎⢿⣝⠄⡾⣿⡏⣥⣶⣾⣿⣶⣬⣭⣛⡻⠿⣿⣿⣮⡑⠎⡚⣿⣿⣾⢙⢿⣿⣿⣿⣿⣮⢻⣷⡜⢦⣶⡦⡙⢤⣝⣻⢿⣯⡀⡰⡌⣿⡐⣻⣝⠊⣿⢦⡘⢷⡕⡥⡝⢿⣮⢹⣷⣂⠻⣯⡘⢿⣷⣮⡻⢿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣗⣛⣿⡾⢛⣵⢚⣥⣿⣿⣷⣾⣿⣿⣻⣿⢃⣼⣿⢰⢸⣿⡟⠡⣾⡿⠋⣠⣾⠿⣼⠏⡵⠐⠋⢘⣡⣶⡙⣰⣶⡶⠞⣛⣣⣭⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠸⣶⣾⡟⠠⣿⠋⠐⡠⠀⠟⡅⣿⠋⡎⣰⡿⢣⠞⢗⣤⡟⡴⡸⣻⣣⣿⠿⠋⠵⢊⣼⠟⡡⠂⢿⢣⢿⡇⠐⡋⠀⣿⣯⠀⢹⢳⣼⡿⣌⣿⡞⢌⠻⣿⣔⢮⡛⠿⢘⠠⣧⢣⢡⢻⣧⠰⡅⣙⢧⣦⢻⡘⡟⢈⡏⢰⢈⠀⢿⣯⢀⢻⣿⣷⠎⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣭⣟⡛⠶⣶⣶⣾⡿⢛⣃⣐⠟⠿⠛⣏⢲⣝⣿⣎⢫⣿⣻⣜⠻⣿⠘⡇⣐⣿⣿⣿⣶⢽⣿⣷⣾⢂⣉⠨⠑⢜⡪⣷⣽⣿⣦⣐⣬⣟⣿⣌⢻⣯⡻⣧⣝
⣽⣿⣿⣿⣿⣿⣿⣿⣿⢟⣩⣶⣫⣴⢫⣿⣿⢻⣩⡾⢟⣩⠖⠁⣾⣏⢋⢈⣧⡟⣡⣤⣿⠅⣀⠋⠀⢸⢋⣄⣶⣶⣾⡿⢟⣛⣉⣬⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣿⡇⢥⡏⡆⣼⠃⡆⠀⢷⢠⡞⠀⢰⠆⠀⠔⣫⢋⢀⡴⣳⡟⣨⢷⢎⠖⠰⢟⡹⡂⢁⠰⠎⢈⢊⣴⣦⠃⠀⢺⡇⠸⢰⢸⣧⡹⠌⠈⠆⣈⢛⢮⡻⠇⠲⡜⡎⣁⠻⣆⢧⡁⠛⣄⠇⠈⢰⣬⢡⣱⡀⢸⠀⢸⡼⣆⢠⢹⣞⢸⣿⡟⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣯⣝⣛⡿⢭⣿⣷⣦⣤⣬⢘⢻⡈⣿⠃⠹⢹⣧⠀⢻⣷⠡⠙⣿⣿⡇⠻⣓⡾⣿⣛⢾⣿⣧⡙⢦⡹⠆⣿⠿⣧⡀⡋⣙⢿⣿⡳⣆⡐⢌⣳
⣟⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣩⣥⡽⢾⡋⣴⡿⠋⣰⣿⠏⠐⢃⣵⡷⢀⣾⠟⢀⢛⠛⠂⡈⡏⠠⠰⣃⣿⠟⣛⣭⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡈⣿⡟⡸⢠⢰⣧⢣⠐⣄⡘⢸⣿⣷⣾⢣⡖⠉⣠⣧⠟⢵⠏⡴⣫⣴⢈⠀⣼⠁⣴⣷⠁⠠⢃⠀⣿⠇⡟⠄⠃⣎⣃⠁⠀⣸⠸⣼⠰⡘⠆⣟⢾⣥⡻⣧⠀⡙⣦⣝⠦⠹⡄⠉⣐⠈⠛⠲⡙⣇⠾⡿⠇⣠⠀⠎⡿⡿⡆⡞⣇⢻⣟⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣬⣙⣻⠿⣿⣧⠁⡈⠐⠷⠌⠻⡤⣆⠻⣧⣆⢿⣿⡻⢦⡘⣷⣦⡝⢿⣮⣛⢷⣀⣯⠻⠿⣿⣮⣽⣎⠻⣷⡍⠻⣌⠯⣅⠾
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣛⣷⣿⠾⠛⠴⣛⡫⣡⠔⣩⣵⠟⢐⣸⡏⣰⡾⠊⣱⣿⣋⣴⡶⢛⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠿⠀⢡⡿⡎⢿⡼⣀⢠⠁⢸⡿⠘⡏⣘⠃⡀⡝⣥⠆⣠⣼⡞⡡⠁⠈⣼⡇⣼⣯⠣⣠⢆⡆⢃⠈⢼⠃⡆⠈⢹⡏⢆⢸⠇⣧⢨⣜⣿⡼⣜⠜⢿⣴⢸⣆⠳⡟⢫⠳⡄⢀⠰⣼⢆⢀⠀⣗⢸⠇⢠⣧⠹⡁⡀⣿⠇⠀⢺⡌⠸⡟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣝⡲⠶⢠⣈⣦⣤⠰⢦⡆⣟⣏⡄⠻⣟⢿⠷⣌⢻⡧⣤⡻⢿⣕⣾⡿⣿⣷⣶⣶⣭⣃⡙⢬⣛⢦⣉⠷⣈⠻
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣶⣿⡿⢃⣐⡀⠠⡶⣂⠈⣡⡾⢫⣵⣿⡿⢫⡄⠋⣴⡇⣿⣿⡿⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⢉⡜⡀⢇⠸⠇⣿⣼⢸⢸⡇⠘⢺⡏⢸⡇⠇⢋⢊⣵⢋⡘⠀⢠⠎⣀⡴⢃⡏⢸⠋⣼⢣⡟⠀⣼⢀⣧⠀⢸⡇⠈⣿⢀⢸⠸⢿⣹⣷⠛⣧⢸⡿⢦⡓⢱⡜⣦⣧⡑⣮⡳⡹⢸⢠⡄⠛⡇⠀⣾⡟⡆⣧⣧⠹⢠⡈⠂⢦⡻⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣌⠹⢿⣿⣦⣠⣙⣻⣻⣷⣅⠻⣙⢿⣎⠳⡍⢆⣉⠤⠮⡛⣣⣾⣍⡛⢿⣿⣾⢻⣷⠽⢟⣿⣿⣾⣝
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢍⠉⣠⣽⠞⠱⠆⠠⣀⡾⣫⣾⣿⠿⢋⡼⣿⣿⣿⣿⣷⡿⢋⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠊⣷⠃⠟⢠⢠⡈⣿⣸⢘⣿⢠⢙⠃⡿⠣⡄⣩⠜⢱⢋⣠⢂⢀⠾⣿⠵⡿⠁⣻⠘⣏⢻⣇⡄⡟⠄⡏⡤⠸⠇⢠⢹⡸⢃⢴⡼⣿⣼⠇⢻⠎⠿⠫⣏⠃⡰⡜⣆⠙⡌⢳⣝⢸⣜⢁⠘⠀⠀⡿⠁⡇⣟⢘⡀⡘⠳⢸⡄⠳⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣌⠻⣿⣿⣿⢸⣿⣷⣝⢿⣆⠌⢛⢷⡝⢷⣍⣥⡸⣆⡢⠛⡿⠻⢿⣧⣭⣿⡮⣝⢿⣭⡺⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡷⠛⣉⣼⣿⠇⢊⡠⠠⠎⣡⣴⠿⢃⣦⣴⠏⢹⣿⣿⣿⡿⢟⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣬⠀⡟⡤⣐⢀⠾⠁⠟⠃⢸⢊⣿⢸⠀⣦⡅⡄⣤⢠⡎⣿⢋⡞⡾⣼⡏⢈⡔⢞⡏⣿⠟⣸⣝⣇⡇⣼⠁⠃⣼⣧⠘⠈⣧⢸⢸⣿⣇⢹⣦⢸⡅⣠⠃⢿⣦⢳⢳⡸⣇⣡⡜⣮⠈⠃⢠⡄⣇⣿⡹⣧⠷⡿⠘⣧⠁⡂⣇⢿⠨⣄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡁⠍⢿⣿⣿⣿⠿⣦⣙⣥⢠⣂⠙⠳⣝⠈⠻⣾⣿⣷⡘⠶⣄⣙⠿⠾⣿⣿⡿⢮⣽⣚⣭
⣿⣿⣿⣿⣿⣯⣿⣯⣾⡿⠿⢟⣡⣶⣿⣠⣤⠿⢋⣵⠾⣿⡟⣡⣾⣿⣿⡿⣻⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠉⡈⢰⣡⠏⢀⣴⠄⢠⡞⠇⣟⡟⠸⢣⡿⠁⠃⠇⣿⡟⢃⣸⢱⣿⠛⢠⡿⢃⣼⢠⠁⡐⣽⢸⡇⢰⡟⡀⢂⣿⣿⠀⠀⢿⡄⣼⡇⢿⢨⢿⡇⣷⡹⣷⡜⣿⣾⡎⡃⠹⣿⣷⠸⠀⢀⣿⠸⡏⣿⣧⢻⣧⠁⠢⣏⠄⢻⡼⠎⣃⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡱⢿⡿⢿⣆⣌⠻⣿⢿⣽⡟⣶⣌⡃⢑⡈⡙⢿⣿⣶⣦⣝⢣⡷⠽⣯⣽⡢⢍⠻⣝
⣿⣿⣿⢟⣿⣿⣿⡟⠛⣀⣴⡿⢻⠿⠛⣉⡤⢰⠟⣱⠾⠟⣿⣿⠿⠛⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠃⢫⡏⠐⣾⡁⢠⡾⠁⣼⢯⢣⢇⣿⠇⣠⣾⢠⠻⠃⢸⢇⡞⣹⠀⣸⢀⡈⢁⣤⢫⢸⠃⡞⡡⠋⠀⡸⢸⣼⡿⠀⣄⢳⣹⣌⢿⡼⣧⣝⣈⠈⢃⡁⣧⠹⡇⢶⡽⡇⢻⠏⣤⣶⡄⢹⣷⢸⢸⣿⣌⢿⣧⠑⣿⡇⣄⣷⠠⢻⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⠻⢿⣿⣷⣻⣷⣍⢻⣮⢙⡻⠾⣿⡷⣶⣍⠻⣿⣿⣷⡍⣋⠿⣽⡛⢦⣵⣝
⠿⣫⢳⣿⣿⣿⣿⣷⣾⠟⣫⡞⠑⡂⣈⡥⢀⣤⣼⣿⣿⡿⢟⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⠀⣾⡁⣾⡋⢄⣼⡷⢰⣽⢈⡆⡘⡏⠀⣿⡏⡼⠏⡔⠸⣼⢁⡏⡼⡡⢿⢰⢸⢹⣼⡏⣠⢶⢿⡗⡠⡁⠂⢿⡇⠐⢬⣎⢿⣿⣷⡅⢻⣾⡏⡇⡏⣿⠜⢇⢻⡘⡇⠃⢠⢰⢻⢿⡓⠀⣿⠀⢦⢹⣿⡎⣿⣧⢬⡳⠣⡿⢇⢸⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣝⠻⣿⣿⣭⣧⣬⡃⣙⠿⠾⣿⢾⡿⣷⣮⣙⠿⣿⣿⣗⣔⠻⢗⡂⢿
⣯⣿⣿⣿⣿⣿⣿⣯⣥⣹⢟⣶⣼⣿⣿⠟⢛⣫⣭⣥⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣾⠀⡿⣠⣿⢃⣾⡿⢡⣭⡏⠘⣼⡏⠅⠘⡿⣸⡷⢸⢃⠇⡏⣼⢠⢨⣴⠉⠘⡾⢸⠟⡕⠟⡼⠏⡼⢣⠰⠀⢎⠱⠁⣸⣿⠧⢻⣷⠻⣈⠛⡇⣧⠁⣿⣮⡃⢸⡇⢻⠸⡾⡇⣾⡀⣧⠀⢼⡆⣌⠃⢩⣁⠸⣿⣧⢹⡶⡈⡏⣻⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣝⣛⠿⠿⢿⣶⣟⣦⣻⣇⣯⣶⣽⣿⣷⣮⣉⣻⣿⣮⡴⠤⣀
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⢛⣛⣭⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣷⡆⢇⣿⠃⣾⢟⣵⢿⡟⡇⢰⡏⢁⣄⡼⠁⡟⡅⢁⠏⡘⢣⡟⣈⢺⡿⡀⡸⢁⡞⢰⣇⠰⢠⠀⠃⡌⡆⠃⣼⠄⠐⣿⢹⢙⢢⡐⡇⣿⡆⢷⠘⡆⠈⣿⡟⡀⢴⡼⠆⢳⡸⢹⢧⠐⣆⡈⡻⢻⡀⣯⢹⣷⡝⢿⣇⠻⣆⢸⣻⡅⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣭⣛⡻⠿⣷⣽⣷⡿⣷⣿⣿⣿⣿⣿⣿⣦⣰
⣿⣿⣿⡿⠿⣋⣥⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⠁⢸⡿⠘⣯⠖⠀⡌⡰⠀⠘⢠⣾⠏⢸⢇⡄⣠⢋⠄⣸⡟⣸⠋⣤⠁⢰⠁⡼⢠⠟⢣⡇⡈⡰⠱⡄⡇⣆⢾⡦⣰⢹⣆⢸⣌⢣⢹⡜⠡⡌⣧⢻⡇⠈⣆⢻⡆⢷⡌⢠⡳⡈⢦⢸⠀⣷⡇⠙⡇⠘⡎⣟⢇⢧⡻⠟⣎⠀⢙⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣭⣝⡻⠿⣿⣿⣿⣿⣿⣿⣿
⢛⣉⣥⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣻⠀⡸⢇⣸⡿⠀⠀⢜⡡⣠⢀⣼⣿⢀⣾⡌⣼⠇⠏⡘⣟⣴⠋⢸⠃⢨⣦⠦⠐⢣⡁⠈⢀⣥⡇⣰⡁⡇⠊⡌⢡⡠⣿⣬⡌⡿⠈⠈⠇⣔⡌⠈⣶⣤⡁⣻⡇⠹⣎⣷⢀⢻⡺⣎⢷⠳⢻⣿⢇⠰⡐⣜⠎⠊⡘⣿⡆⠾⠁⢸⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣛⠿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣽⣿⣇⠁⣿⡗⠡⣀⡽⣠⣶⠸⡹⢣⡞⣽⣾⢗⣀⡚⣁⣿⠃⢠⠃⢰⡸⢡⠂⣀⡿⡡⢣⢸⢹⣿⣾⠇⠏⠀⡀⢈⠁⠿⢸⣇⡙⡧⣇⡼⡌⢷⡀⢸⡼⣧⠀⢷⡔⡹⣯⡀⢆⣳⢾⡾⣦⠣⠹⡎⢵⣮⡒⣆⡠⣕⢿⡿⠡⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣍
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣋⣇⡿⠋⠀⣤⣶⣷⠿⡫⠀⣴⡟⡼⢻⠋⣩⢏⣼⢿⠃⡀⣻⠘⢸⢰⡿⢳⡿⣡⠇⣾⢸⣾⡿⠃⣸⠘⡦⠳⠎⢶⠀⡇⢸⣧⣟⠻⣧⢸⣤⢷⡸⣿⠹⣧⢸⣷⡙⠫⣿⣮⢻⡥⢻⡀⣬⣷⡄⠨⡛⣷⡙⡦⡀⣿⡳⡁⣿⢻⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠠⣼⣿⣿⡴⣱⣦⣿⢟⡵⣪⢅⣼⣟⣽⣷⠇⡴⢃⡞⣵⡟⡤⢣⣿⣸⣾⣼⣠⣿⣿⣏⣶⣧⣲⣿⣡⣿⣄⣧⣷⡄⣴⣾⣸⢠⣿⣟⣏⣴⣰⢨⢹⣶⣧⣻⡇⣿⣌⣿⣱⣁⣷⡝⣷⢹⡜⣻⣹⣿⣿⣄⢹⣢⣝⠶⣄⣶⡑⡝⣿⢾⣿⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿''', 0.5)
def village_art():
    echo('''⣆⢻⣷⠙⢿⣿⣿⡇⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⠏⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢿⡜⣿⡇⠀⢿⣿⣧⢻⣿⣿⣿⣿⢺⣿⣿⣿⣿⡿⣫⠊⣴⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢼⡇⠈⡇⠃⠈⠹⣿⡈⣿⣿⣿⣿⣼⣿⠿⠛⠉⢚⣵⣿⢹⡟⣷⠉⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣇⠀⠉⡆⠑⠀⢹⣳⠙⣛⠉⠉⠉⠁⣀⣥⣾⣿⣿⣿⢸⣷⣿⡇⢹⣿⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⡿⣧⠀⠈⡆⠀⠀⠸⣆⢴⣶⣶⣿⣿⣻⣿⡏⣿⣿⣿⡇⣿⣿⣇⢸⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⠀⠀⠹⠀⠀⣾⣿⡞⣿⣿⣿⣿⢸⣿⢣⢿⣿⣿⣧⢿⣿⣿⣮⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⡌⡇⠀⠘⢀⢻⣿⣷⡹⣿⣿⣿⢾⣿⡜⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢠⡤⢠⠄⠀⠀⠸⠀⠈⣿⣿⣷⡹⣿⣟⣾⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿⣇⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠐⠃⢘⡂⠀⠢⠀⠸⣤⠈⢿⣿⣷⡙⡿⣿⣿⣿⡜⣿⣿⣿⣿⣏⡻⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⡇⣾⣿⣤⠀⠛⣆⠈⢿⣿⣿⡔⣾⣿⣯⣿⣦⢻⣿⣿⣿⣇⠙⣿⣯⡄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⡇⣿⣿⣿⣆⠀⠘⡄⠈⢿⣯⣿⡜⣿⣿⣿⣿⡜⠿⣿⣿⣿⡆⣹⣷⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⡇⢻⣿⣾⣿⢀⠠⠙⡄⠀⢰⣿⣿⡼⣿⣿⣿⣿⣿⣾⣿⣿⣷⣾⣾⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⢸⣿⣿⣿⢸⣆⠁⠘⣆⠀⢿⣿⣿⡎⢿⣿⡟⣿⣿⣿⣿⢻⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠘⣿⣿⣿⠀⣿⣿⣿⡄⣿⣆⠐⡘⢣⡀⠙⣿⣿⣮⢻⣇⣿⣿⣿⣿⢿⣿⣿⣷⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠰⣿⣭⣯⣤⣼⣮⣽⣧⣭⣭⣷⣤⣤⣥⣤⣌⡙⣿⣷⡝⢿⣿⣿⣭⣌⣿⣿⣿⡮⣍⠉⠉⠉⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠶⠒⠴⠦⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⠻⣿⣷⣙⠿⢿⣿⢿⣿⡛⣃⠀⣶⣶⣶⣆⣀⡤⣤⣤⢤⣤⣄⣤⣶⣶⣴⣶⣶⣶⣶⣶⣶⣶⣴⣷⡶⢀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⠀⠀⠀⠀⠙⠚⠉⠛⠛⠉⠉⠉⠉⠉⢹⣿⣿⣟⠃⠘⢿⣧⣹⣷⣆⢶⣶⡄⣭⣴⠿⠿⠿⠿⠿⠿⠽⠿⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠀⡀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⢀⣤⣶⣶⣾⣿⣿⣶⣶⣶⣤⣄⠀⠀⠈⠛⠛⢛⠁⠀⠀⣟⣿⣿⣿⣮⣻⠇⢠⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢀⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⡀⠀⠀⢈⠂⠀⣸⢿⣿⣿⣿⣿⡏⣾⢸⣿⣿⡿⡿⢿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⠀⢿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢰⣶⣶⣶⡄⢠⠏⣼⣿⢋⣿⢿⡧⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢠⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠠⡄⠤⡍⢩⣭⣭⢭⣽⣿⣿⣿⣿⣏⣸⣽⣿⣿⣿⠃⠞⢠⠏⢠⣾⢏⣼⠣⠿⡿⣿⡿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣿⣿⣟⠛⡿⢸⢸⠇⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡸⠷⠿⠯⠬⠿⠅⠘⠿⣿⣿⣿⣿⣿⡇⣸⣿⣿⣿⡂⠀⠋⣠⠟⣡⠾⢃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⣼⢀⡀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⡆⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣤⣤⣶⣴⣶⣴⣶⣶⣶⣶⣦⣤⡄⢰⢻⡏⣿⡍⡇⠀⣼⠇⢰⢣⠆⣛⣛⣛⣛⡛⠛⠛⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⢠⢰⡇⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣰⣷⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠈⣼⠇⣿⠀⡇⠀⠛⠐⣸⢏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⢸⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⠿⢶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠁⣿⢐⣿⠀⡇⣀⠢⡀⢿⣾⣬⣭⣭⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡇⠈⢾⢸⣿⡟⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢀⣼⣸⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢀⣿⡴⣿⠀⡇⣿⣷⣌⠢⡙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⡿⠁⢰⡜⢸⣿⣷⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣾⣿⠘⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⡏⣉⠉⠉⠉⠉⠉⠉⠉⢙⠉⠛⠛⡛⠛⣛⣛⢛⣛⣛⣛⣛⣛⣛⣛⣛⣿⡿⠟⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⣶⢸⣿⣯⣿⡀⡇⣿⣿⣿⣷⣌⠢⡐⢶⣶⣶⣤⣤⣴⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣶⡦⢸⢸⡇⢸⣿⣿⡆⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⡇⣿⣛⣛⣀⣀⣀⣐⣒⣋⣛⣛⣛⣋⣙⡙⠃⠀⠘⠾⠿⠻⠿⠿⠿⠿⠾⠷⠐⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⢸⣿⡿⣿⡇⡇⣿⣿⣿⣿⣿⣿⣯⡢⣝⢻⣿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⢿⣿⣿⡿⠿⠇⠈⣼⠙⢸⣿⣿⡇⡌⠙⠛⠛⠛⠛⠛⠛⠛⠛⠀⠀⠘⠋⠛⠛⠋⠉⠉⠉⠉⠁⠈⠉⠉⠉⠉⠁⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡶⢀⡹⣿⣿⣿⣿⡿⠯⠽⠿⡇⣆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⡇⣿⣿⠁⢿⣿⣿⣿⣿⣿⣿⣿⣶⡄⠉⠻⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⢂⣿⠀⡏⣿⣿⡇⠀⢸⣿⣾⣾⡷⠶⠿⠟⠤⠀⠀⠈⠛⣡⡶⠗⣀⠠⠶⢷⣢⡶⣒⠶⠶⣶⣤⡴⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣷⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠿⣿⣟⢠⣏⢧⠹⣿⣿⣿⣿⣿⣿⣿⣧⠻⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⠀⣿⠙⡄⠀⠒⠒⠒⠒⠒⠚⠋⠁⠁⠸⢠⣿⣿⣿⣿⣿⢿⣛⢻⣿⣻⣛⣻⣟⠛⢛⣛⣛⣛⣛⣻⡃⢀⢸⣿⠀⡇⣿⣿⣿⢸⢨⣭⣽⣿⣷⣭⣤⣡⠄⢀⠀⡀⣷⠈⠡⣿⠿⢶⡬⠌⠡⠴⠷⠷⢦⣦⠿⠒⡇⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⡛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣼⡿⢋⣾⣿⡜⡇⢿⣿⣿⣿⣿⣿⣿⣿⡨⡈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣸⣿⡄⣿⡂⠹⡄⠘⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠈⢸⢹⠀⡇⢸⣿⣿⠈⡞⣿⣿⣿⣿⣿⣿⣷⠀⢸⠀⡇⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢃⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣯⣭⣽⣾⣯⣴⣿⣿⣿⣿⣿⣿⣿⣙⣛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠻⠻⠻⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠏⠼⠟⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣷⣴⣾⣶⡿⢁⣼⣿⣿⣿⠅⣸⣿⣿⣿⣿⣷⣿⣿⣆⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠐⣄⢍⡍⠁⣍⣩⣉⣉⣉⣉⣉⣁⠀⢻⣿⢐⣿⠀⡆⣿⡄⠘⣿⣿⣿⣿⣿⣿⡇⠠⢸⠙⣿⣿⣿⣿⣿⣽⣿⣿⣿⣏⣍⣩⣭⣭⣉⣍⣭⣉⠉⠁⠀⣧⣾⠀⡇⢸⣿⣿⡇⡇⢻⣿⣿⣿⣿⣿⡟⠀⣾⠀⣧⢻⣿⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣾⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡇⣿⣶⣶⣿⣿⣾⣦⣤⣗⣴⣎⣨⣠⡈⠀⠀⠀⠀⠀⡀⠀⠀⠉⣉⣉⣯⣽⠛⠻⡋⠁⢻⣧⢸⣿⣿⣿⣿⣿⣿⣿⣶⣦⡶⠟⣱⣿⣿⣿⣿⡏⢰⣿⣿⣿⣷⣿⣿⣾⣾⣿⢸⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠨⠿⠿⠏⠉⠛⠛⠑⠿⠿⠿⠿⢿⠀⢸⣿⢸⣿⠀⠇⣿⣿⡄⠸⣿⣿⣿⣿⣿⡇⢀⢸⠀⠿⢿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠿⠿⠯⠉⢁⡮⠀⣼⣾⢸⣿⠀⢧⠀⣿⣿⡇⢧⣸⣿⣿⣿⣿⣿⡇⢠⣿⠀⣿⡘⣿⡇⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢠⣹⡀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣍⣭⣉⣁⣉⠉⢉⣉⣉⣈⣉⣙⡿⣿⡟⢛⢛⠋⠘⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⡶⢃⣼⣿⣿⠃⣶⣦⠀⣾⣿⡿⠿⢶⣶⣶⣿⣿⣿⡄⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣴⣿⣷⣿⣷⣶⣶⣶⣶⣶⣶⣶⣆⢸⣿⡟⣿⡆⢀⣿⣿⣷⡄⠹⣿⣿⣿⣿⡇⠘⠈⣦⢶⣴⣶⣤⡤⠆⠀⠀⠠⠤⠇⠴⠆⠤⠴⠁⠴⣦⠘⢿⣿⣿⣿⣯⣾⠀⢹⣿⣧⢸⡏⣿⣿⣿⣿⣿⠁⠀⣿⠀⣿⡷⢹⣿⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣰⣄⠉⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣻⠇⡞⣆⢻⣿⣛⣛⣿⣟⣛⠛⢚⠒⠒⠂⢻⡇⢹⣿⣿⣿⣿⣿⣿⠌⢡⣾⣿⣿⣿⠀⣿⠏⣴⣿⣿⣿⡿⢶⡶⢀⣀⣒⣒⣂⠈⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⢸⣿⣷⣿⣿⢸⣾⣿⣿⣷⡄⠹⣿⣿⣿⡇⠀⠀⣬⣭⣭⣭⣥⣍⡈⠁⠠⣤⣤⣤⣤⣤⡀⢀⠀⠀⠀⠀⠘⠁⠈⠀⠸⠣⡆⢸⣿⣿⢸⡇⢿⣿⣿⣿⣤⢠⡀⢠⠀⢠⠀⡇⢛⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣷⠀⠐⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣋⣵⣾⣿⡄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣛⣛⣓⡻⢋⣾⣿⣎⣆⠻⣟⢿⣷⣿⣾⠟⠾⠿⠷⠶⠸⣿⠸⣿⣿⣿⣿⡿⠀⣴⣿⣿⣿⣿⣿⣤⡏⢠⣿⣿⣿⣿⣿⣵⣦⢄⢤⣤⣤⣦⡀⡄⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⢸⣿⣿⣿⣿⣷⡀⠛⣿⣿⣷⢸⠀⣿⣿⣿⣿⣿⣿⣷⠀⠀⣿⣿⣿⣿⡿⡀⡘⠿⣶⠀⠈⠀⠀⠀⠀⠠⣶⣶⣾⣿⣿⣇⢻⡌⣿⣿⣿⡿⢸⡇⢸⠀⢸⠀⡇⢸⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣒⠉⠻⡀⠂⣭⣭⣉⣥⣭⣤⣤⣴⣶⣿⣿⣿⣿⣿⣿⠹⣿⣟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣹⡇⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⡛⢃⣴⣿⠟⡛⢿⣮⢳⡙⢛⣛⠟⡿⠿⠿⠷⠶⠒⠀⣿⡇⢿⣿⠿⣃⠴⠞⠛⠛⠛⠛⠛⠛⠋⣠⣸⣿⣿⣿⣿⣿⣿⣿⣆⢦⣅⡳⣾⣇⢹⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀
⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⡜⣸⣿⣿⣿⣿⣷⡀⢹⣿⣿⢸⣆⠻⣿⣿⣿⣿⣿⣿⢀⣾⣿⣿⣿⣿⡇⡇⣇⣿⣆⠘⡆⢠⣘⣿⠀⢩⣭⣭⣭⣭⣭⣍⡉⢃⣿⣿⣿⣷⢸⡇⢸⠀⢸⠀⡧⢸⢁⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⢀⣿⣿⣦⠀⠀⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⣿⣿⣷⣾⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡇⣷⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⢃⣴⣿⣿⣿⣜⢿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣤⣶⣶⣴⣶⣦⣤⣦⣴⣤⣴⣦⣭⣭⣤⣦⣤⣴⣶⣶⣤⣶⣶⣶⣶⣷⣶⣶⣾⣗⠙⠋⠉⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀
⢰⣦⣶⣦⣤⣤⣴⣤⣬⣿⣿⣯⣷⣶⣮⣽⣿⣯⣴⣟⡋⢿⣿⣿⣿⣿⣧⡀⢻⣿⢸⢿⣷⣈⢿⣿⣿⣿⣿⢸⣷⣿⣿⣿⣿⣧⡇⣿⠉⠈⢁⡧⣿⡿⢿⡄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢀⣶⣦⠀⣶⢶⠆⢀⡘⠿⣿⣿⣿⣿⣿⡟⠋⠱⣶⡎⠻⣻⣿⣀⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢿⣿⣿⣿⣿⣿⣾⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⠃⣿⠸⣿⣿⣿⣿⣿⣿⣿⠟⢛⣱⣿⡿⢹⣷⣿⣿⣷⣾⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣯⣍⣁⣬⣤⣤⣾⡲⢣⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⡀
⢠⣯⣿⣭⣿⣯⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠘⠻⠿⠿⠿⠿⠇⠀⠛⢸⢻⣿⣿⢸⣿⣿⣿⣿⢺⣿⣿⣿⣿⣿⣿⡇⡏⠀⡄⢸⣷⣿⠀⠀⣁⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠙⢃⣿⣶⣶⣶⢸⠻⠀⠉⠉⠉⠉⠉⠀⠀⠀⠁⠀⠀⠀⠈⠉⠋⢸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⢀⡿⠀⢽⡀⣿⣿⣿⣛⣛⣛⡀⣒⣉⣁⡉⡅⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠃⢢⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⣠⣾⣆
⠨⠿⠿⠿⠿⠿⠿⠿⠿⠟⢿⣿⣿⣿⡻⢿⣿⣿⣟⡛⢉⣴⣶⣶⣶⣶⣶⣶⣤⣤⢸⢸⣿⣿⢸⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⠁⡇⠀⠇⢿⣿⡇⠀⠀⢸⢀⣀⡀⠀⠤⠤⠴⣶⣤⣤⣤⣤⣤⠀⠀⣸⣿⣿⣿⣿⢸⣤⡀⠀⢀⣀⣀⣀⠀⠀⠀⠀⠶⡄⠀⠀⠁⣬⡘⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡽⣿⣿⣿⣿⣿⣿⡇⣸⡇⠀⠈⠗⢹⣿⣿⣿⣻⣿⣿⣿⣿⣿⠃⠧⠈⣿⣿⣿⣟⣻⣿⣷⣶⣶⣷⣾⣿⣿⣷⡶⣿⣬⣭⡿⣿⣿⣭⢽⣿⠭⣍⣭⣭⣭⣿⣯⣭⣭⣿⣿⣿⣿⢋⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣘⣷⠈⠳⡜⢿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⢀⣴⣿⣿⣿
⠀⢀⣴⣶⣶⣶⡤⠀⡀⠀⣿⣿⣿⣿⣷⠀⠀⢀⡉⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⠀⣿⣿⢸⣿⣿⣿⣿⠸⣇⣿⣿⣿⣿⣿⠀⡇⠀⠀⢸⣿⡇⠀⡇⢸⡈⢿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣦⣤⣤⣭⣍⣙⠻⢿⣿⢸⣿⣇⠀⢸⣿⣿⣿⠀⠀⠀⠄⡀⡆⣆⣠⠀⢄⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡹⣿⣿⣿⣿⠀⣿⠇⡆⣿⢰⡈⠛⠛⠿⣿⣛⢛⠻⣿⡃⡀⣖⠀⣿⣿⣿⣿⣯⣭⣭⣭⣭⣩⣭⣭⣝⣛⣛⣛⣛⣛⣛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢀⡀⠀⠀⠀⠀⣧⠙⢧⡙⢿⣿⣿⣿⣿⠟⠁⠀⠀⣠⣿⣿⣿⣿⣿
⠐⣿⣿⣿⣿⣿⣿⣼⣷⠀⠋⢿⣿⣿⢃⡗⠚⠉⡇⠃⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠘⠀⣿⠛⣸⣻⣿⣿⣿⠀⠇⣿⣿⣿⣿⣿⠀⠀⠀⠀⠸⣿⣇⠀⠀⢸⣇⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣶⣤⣼⠿⢿⠆⢸⣿⣿⣿⡀⠀⠀⠀⡇⠀⣿⣿⡏⠂⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠫⣥⣿⣿⣿⡟⢠⠿⠘⠀⠈⠀⠙⠂⠙⠀⠀⠶⠄⠾⠾⠧⠁⡏⡗⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⢡⣿⣿⣿⣿⣿⣿⣿⣿⣽⡿⠋⠀⠐⢚⣃⣀⣀⣀⣀⡙⠀⠀⠙⢦⣝⠿⡿⠉⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿
⠀⣿⣿⣿⣿⣿⡿⣿⣿⠀⠀⣿⢿⣿⢨⡇⣶⡶⡶⠶⠶⢶⣶⣶⣶⣮⣤⣤⠄⠀⠀⣠⣵⣾⣿⣿⣿⣿⣿⠂⠁⣿⣿⣿⣿⣿⠀⠀⠀⢳⣴⡝⡿⠀⣄⢸⠇⣴⡹⣿⣮⣙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣾⣅⠸⢿⣿⡿⠁⠀⡀⠀⣇⠀⢿⠉⢥⠈⠁⠉⠉⠉⠉⠉⠉⠉⠉⠉⠛⠛⠋⠛⠋⣩⣭⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣴⣦⣽⣿⣿⣿⣧⣶⣶⣶⣶⢰⣦⠀⢸⢧⢸⣿⣾⠀⠟⡿⠇⠀⢳⢉⠈⣿⣿⣿⣿⣿⣿⣿⣿⡿⠯⠽⠿⠿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣻⢟⣵⣿⣿⣿⠿⠿⣿⡿⠏⠉⣭⣾⣾⣿⣿⣿⣿⣿⣿⡿⠋⠀⠙⢄⡀⠀⠙⠃⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⡿
⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⡿⠸⠇⠀⠀⠀⢠⣴⣿⡿⢟⣩⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⡇⣿⣿⣿⣿⣿⡅⢻⣿⣦⣿⡁⣧⣦⣸⠂⠀⣿⣿⣿⣿⣿⣿⣮⣛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⡀⠀⠀⠛⠃⠙⠶⠾⠁⢈⠀⣶⣶⠆⢰⣶⣶⣦⢰⣶⣶⠀⣰⣶⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⠉⡀⠀⢸⢸⣿⣿⣾⣿⡷⠀⡀⡈⣍⠀⢻⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣽⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣯⣶⣿⣿⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠀⠀⡀⠀⠀⠙⠢⠄⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡅
⢸⣿⣿⣿⣿⣿⣿⣿⣿⠂⠀⣹⣛⣿⠀⡀⠀⢀⡴⣻⠿⢫⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⡇⣿⣿⣿⣿⣿⡇⣼⣿⣿⣿⡔⣿⣿⣿⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⣧⣷⣷⣶⠀⡀⠀⣿⣿⠈⢸⣿⣿⣿⢸⣿⡇⡇⢻⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⡇⢀⣤⣾⣿⣿⣿⣿⡇⡰⢀⠇⠛⢠⡈⣿⣿⣿⣿⣿⣿⡿⣿⣿⣯⡭⢽⣿⣿⣿⣿⡛⢻⣿⣿⣿⣿⣿⣿⣷⣾⡛⠛⠛⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⢀⣠⣤⣤⠀⠀⠀⣶⣶⣶⣶⣶⣦⣤⣤⢸⠈⣽⣿⣿⣿⣿⣭⣭⣭⣤⡄
⣸⣿⡟⠋⠉⣭⠭⠭⢭⣤⠀⣿⣿⣿⠄⡀⡴⣫⡾⠫⠾⠿⠿⠟⢛⣛⠛⠿⠿⠿⠟⠛⣛⡛⠻⠻⠟⠟⠛⣠⣅⠛⠋⠛⠛⠃⠀⢿⠿⠿⠿⣧⣿⣿⣿⣇⡀⠿⠿⠿⢿⡿⠟⠿⠿⠟⢿⠿⢷⠌⠛⢿⣿⣯⣻⣿⣿⣿⣯⣿⢿⣿⣿⣽⡿⣿⣿⣿⣝⠛⢛⣠⣤⠀⠚⢛⣐⠀⣛⠛⠋⠀⠛⣛⡀⠘⡛⠃⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣠⣷⣿⣿⣿⣿⣿⣟⣋⠀⡀⠾⠟⠧⠸⠷⠀⠀⠠⠀⠤⠤⠭⠌⢉⣭⣽⣿⣿⣿⣿⣿⣿⣷⣌⠹⠯⠭⠯⠯⠭⠍⠁⠀⢠⣤⣤⣤⠀⢀⣤⣤⣤⡄⣠⣠⣠⣀⡀⣠⠀⢸⣿⣿⣿⠀⠀⠀⠛⢛⠛⣛⣛⣹⣭⣥⢈⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣽⠏⣰⡶⢾⢿⠁⠀⠺⣿⠰⣿⣿⣿⠀⡇⣵⣟⠛⣰⣾⣿⣿⣷⣘⣛⣧⣶⣶⣶⣶⡦⣛⣋⣤⣶⣷⣶⣦⣙⣊⣠⠀⣧⡆⠀⠀⠘⠀⠃⠘⠶⠟⠴⠂⠉⠉⠀⠀⠐⠲⠶⢶⠄⣤⣤⣤⣄⣤⣄⡀⠀⠉⠉⠁⠈⠉⠉⠉⠛⠉⠛⠛⠙⠛⠋⠛⠛⠛⠛⠆⣱⢸⠀⠿⠎⠛⠀⠋⠴⠷⠐⠷⠝⠇⠀⠡⠦⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⣸⣭⣽⡿⣛⣭⣾⡿⣛⣭⣾⣿⠀⠀⢰⣤⡔⠲⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⡟⠋⠉⡁⠀⢈⠙⠻⣷⡄⠀⠀⠀⠀⠀⣼⠀⢸⣿⣿⣿⠀⢸⣿⣿⣿⡇⠏⠛⠛⠛⠀⣿⡇⡌⣭⣭⣭⠀⠀⠀⠀⠜⢰⣿⣿⣿⣿⡏⢸⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣃
⢡⣾⣿⣯⣿⣽⣤⣤⣴⣿⠀⣿⣿⣿⢠⣇⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⡿⢟⣭⣭⣬⣝⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡗⡄⣤⣤⠄⠀⠀⠘⢿⣿⣿⣾⣾⣿⠆⢠⣿⣿⣿⣧⣜⢿⣿⣿⣿⣿⡇⢠⠀⠀⠐⠋⠀⠀⣘⠸⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠚⠛⠘⢀⣤⣤⣤⣠⣤⣤⣤⣤⣤⣤⣄⡄⠀⡀⣠⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣤⢩⠙⣉⣉⡉⢩⣭⣤⡍⠉⢁⢀⣠⣤⡄⠀⣸⣿⢡⣦⠀⠀⠀⠀⠀⣼⣿⣿⡿⠣⠾⠿⢣⡈⠿⠆⣆⡀⠈⢿⡀⠀⠀⠀⠀⢹⡇⢸⣿⣿⣿⠀⢸⣿⣿⣿⡇⢴⣦⠀⣴⠀⣿⣧⢁⣿⣿⣿⣶⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⢸⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⣤⣤⣤⣄⣄⣀⣀⡀⠂⠿⠀⣹⣿⣿⢸⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⡿⣴⡟⣩⣴⣶⡝⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⡇⣧⡟⠁⣠⡆⣰⢰⣦⠙⣿⣿⣿⡇⠀⠈⢻⣿⣿⣿⣿⣷⣝⢻⣿⣿⣿⠈⣤⡀⠀⢠⣤⠀⣿⣿⣿⣷⡇⣦⣤⣤⣤⣤⠀⠀⠀⡀⠰⠿⠿⠿⠟⠛⠛⠛⠛⠛⠛⠛⠿⠇⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⠉⢁⡇⢸⣿⣿⡇⣾⣿⣿⣿⣿⡇⠀⢓⡇⢾⢯⠀⠀⠀⠀⠀⣿⣿⣿⠃⡤⠄⠀⠀⠤⠀⠀⠄⣶⠀⠀⡄⠀⠀⢀⠀⢸⡇⠈⣯⣭⣥⣼⢸⣿⣿⣿⡇⢹⢱⠂⢰⠀⣿⣷⣶⣿⣿⣿⣾⠀⠀⠀⠀⠸⣿⣿⣿⣿⡿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣡⠄⠀⢹⣿⣿⢸⣇⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⣿⢡⣿⣿⣿⣿⠘⣷⢸⣿⣿⣿⣿⣿⣿⣿⡇⣿⡇⠋⢠⡶⠏⠀⠻⠈⢡⣾⡊⠻⡿⠀⠀⠀⠈⢻⣿⣿⣷⣶⣶⣦⡙⠟⡇⢰⣿⡇⠀⠸⣿⠀⣿⣿⣿⣿⡇⣿⣿⣿⣿⣟⠀⠀⠀⠗⠀⠀⠀⠀⠀⠀⠀⠀⢀⣄⣀⣢⣶⣶⠀⣿⣿⣿⣿⣿⠿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢸⣿⠀⠸⡇⢸⣿⣿⡇⣿⣿⣿⣿⣿⡇⠀⣸⢡⠏⡟⡆⠀⠀⠀⠀⣿⣿⣟⡌⣴⠂⠀⣹⡾⠀⣄⡇⢿⠀⢰⡆⠀⠀⠛⠃⢸⡇⠘⣿⣿⣿⣟⢸⣿⣿⣟⠃⠈⠀⠀⠚⠀⠛⠉⡬⣭⣭⣭⠹⠀⠀⠀⠀⢠⣼⣿⣿⣿⣤⠁⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣼⣿⣿⣾⡟⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⣿⢸⣟⣻⣿⣿⢰⣿⢸⣿⣿⣿⣿⣿⣿⣿⡇⡏⠀⣀⠀⠀⠈⡉⠀⠀⡄⠀⠀⠀⠀⡀⡰⢾⢦⣷⣎⠛⡛⢉⣉⣉⣉⠀⢹⠀⣿⡇⠀⠀⣿⠀⣽⣿⣿⣿⡇⢿⠛⠛⠛⢳⡄⠀⡆⣾⠀⣆⠀⠀⠀⢌⣂⠀⠽⠿⢾⣿⣿⠿⡄⠻⣿⣿⣿⣶⣾⣟⣿⣛⣛⠿⠿⣿⣿⢿⣿⠿⣿⣿⣿⣿⣿⡟⢸⣿⠀⠘⡇⢸⣿⣿⡷⠾⡿⣿⣿⣯⡅⠀⣷⢙⠀⢣⡇⠀⠀⠀⠠⢻⣿⢻⡇⣿⣄⠆⠉⡴⢣⣿⣇⠀⡀⠿⠁⠀⠀⠀⠀⢸⡇⠀⢉⣭⣭⣬⡜⠛⠛⠉⠀⠠⠰⠄⠀⢀⣉⠁⣧⢹⣿⣿⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⠉⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⣻⣿⣿⣿⡇⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⣿⢸⡿⢿⣿⣿⢸⣿⣸⣿⣿⣿⣿⣿⣿⣿⡇⡇⠀⣿⠀⢸⠀⠀⠀⠀⠀⠐⢃⡀⠀⣏⣀⠀⢸⣿⣿⡇⣿⣿⣿⣿⣿⡐⣄⠀⣿⣧⣀⣰⣿⠀⣿⣿⣿⣿⡇⣇⣀⣀⣀⣀⠀⡇⢡⣼⡄⢿⣶⣶⣦⡄⠀⠀⠀⠀⠀⢰⣶⣶⡀⠿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣶⣾⣿⣿⣿⣿⣷⣿⣿⣿⣷⢸⣿⣾⣿⡇⢹⣿⣿⡧⣿⣿⣿⣿⣿⠇⠀⠀⣼⣿⡞⣇⠁⠀⠙⠂⠀⠛⠘⠧⠿⠿⠀⠘⣱⣿⡿⣿⡇⣧⠘⠛⠛⠀⠀⠀⢸⡇⠀⢸⣿⣿⣿⡇⢈⣀⣀⣀⢠⣥⣠⣄⣸⣾⡀⣿⢸⣿⣿⠀⠀⠀⠀⢀⠑⡈⣿⣿⡇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⠏⠾⠀⠀⢻⣿⣿⡇⡇⣿⣿⢸⣿⣿⣿⣿⣿⣿⡗⣿⢸⠿⣿⣿⣿⣼⣿⣹⣿⣿⣿⣿⣿⣿⣿⡇⣷⡀⣿⠀⢸⣀⡄⢸⠀⣀⣠⣸⣷⡀⣿⡂⠄⠸⣿⠘⢀⠹⣿⣿⣿⢨⢩⡾⠔⣿⣿⣿⣿⣿⠀⣸⣿⣿⣿⡇⣿⣿⣿⣿⣷⠀⡟⠀⣿⠀⠘⣿⣿⣿⡇⠀⠀⠀⠀⠀⠘⣿⣏⠓⢈⣈⡉⠉⠉⠻⠏⠹⠿⠅⠀⠁⠸⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠐⠿⠿⠿⠇⣸⣿⣿⡇⣿⣿⣿⣿⡟⡀⠀⣀⠻⣸⡇⡇⠂⠀⠀⢸⠀⠀⠅⠀⠀⠀⠀⠀⣿⣶⣿⣤⣧⢸⠀⠀⠀⠀⠀⢀⢸⡇⢰⣶⣾⣿⢉⢸⣿⣿⣿⣇⠀⣿⣿⣿⣿⣿⡇⣿⣸⣿⣿⠀⠀⠀⠀⠈⠀⠉⠰⠁⠀⠀⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟
⢸⣿⣿⣿⣿⣿⡇⠘⠔⠀⠀⢻⣿⣿⡇⢻⢹⣿⡎⢻⣿⣿⣿⣿⣿⣿⣿⣭⣭⣭⣭⣭⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⢣⣿⣧⢹⡇⣈⣿⡇⠈⢀⣸⡇⠀⠙⠁⣿⡦⠑⠀⢸⣧⣼⡖⣿⣿⣏⣤⣿⡗⠀⣿⣿⣿⣿⣿⠀⢹⣿⣿⣿⡇⠿⣿⣿⣿⡟⠀⣷⣆⠈⣀⣀⣉⣉⣉⡁⢀⣀⠀⠀⣀⠀⠀⠁⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⢿⣇⣙⣿⣿⠀⠀⠀⠀⠀⡀⠉⠉⠉⠉⠁⡀⠉⠉⠀⠀⢠⣶⡆⣮⠅⠀⠀⠀⠀⠀⠐⠀⠄⠀⠀⠔⠀⠀⢿⣏⠹⣿⡟⠈⠠⠀⠀⠇⠀⠈⡄⠃⠘⠿⠿⠿⢈⠸⠿⠿⠿⠿⢀⣿⣿⣿⣿⣿⣇⠿⠿⠿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⣿⢱⣿⠀⠀⢸⢿⣿⣿⣧⢸⢸⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⣿⣇⢸⣿⣿⣿⣷⠀⢸⠿⠿⠀⠀⣾⣷⣿⣇⠀⠰⣿⣿⡇⢻⣿⣿⡯⠍⠉⢠⠿⠿⠯⠽⠉⠈⠈⠉⠉⠓⠿⠀⠚⠛⠛⠚⠃⣿⣿⣿⣿⣿⣿⣿⢯⣵⢶⡶⢦⡴⢢⠶⣦⡗⣰⣶⢰⡄⣶⣄⣶⣄⣶⣰⣶⣼⢶⣴⣦⡤⢤⣀⣄⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠁⠀⠈⠁⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠈⠀⠀⡀⠀⠀⡀⠀⠀⢀⣀⠁⠀⣤⠤⡤⡤⠀⢤⡤⠤⣤⣤⣬⣭⣭⣭⣉⣭⣋⣀⣀⣀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⣸⣿⣿⣿⢸⢸⣿⡏⣽⣿⣿⣯⣭⣭⣭⣭⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣭⣽⣯⣭⢰⣿⣿⢸⣯⣭⣭⠁⢠⠈⠛⠂⣸⠀⢸⣿⣿⣿⣧⠀⢹⣿⣗⢸⣿⣿⣿⣇⠀⠸⣄⢤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⠀⠷⣽⠿⠿⠿⠿⢿⣿⢟⣱⢟⣵⡿⣱⡿⢳⣯⢁⣿⡯⣾⣧⢾⣧⠹⣿⡜⣿⣎⢿⣎⡑⣏⡙⣋⡙⠓⣈⡂⡉⣀⢈⣙⠛⠛⠛⠛⠛⠛⠛⠛⠙⠉⠉⠉⠉⠉⠉⠀⠀⠀⠉⠉⠈⠀⣉⠁⠀⠀⠁⣀⣀⣁⣀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠃⠈⠀⠀⠀⠁⠀⠀⢀⠀⡀⣀⠘⠋⠀⠀⠉⠉⠉⠉⠉⠈⢉⣉⠀⠀⠀⠀⠘⠿⠃⠟⠿⠿⠿⠶⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⢸⣿⣿⡟⣿⣿⠁⠀⢀⠒⢰⣽⣿⣿⣿⡜⠘⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢸⣿⣿⡟⠀⠈⠀⠀⠀⠹⠀⠸⣿⣿⣿⢿⣧⠀⢹⣿⣸⣿⣿⣭⣥⣤⣤⣿⣾⣿⣦⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣿⣴⣶⣶⣾⢿⣽⢟⣱⣿⢏⣬⡿⣣⣿⡟⣿⣿⡇⣻⣟⢬⣭⣤⢿⣿⡼⣿⣯⣻⣿⣿⢿⣿⡭⣽⣯⡿⣿⣼⣳⣭⠠⢬⣽⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⢸⣿⣿⣿⣿⣿⡇⠀⢸⣷⡆⠂⠀⣠⣤⡄⢠⣦⣤⣤⣄⠲⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣤⣤⣴⣶⣦⣤⠀⠀⠀⢰⣶⣶⣿⣿⣿⣿⣿⣷⠀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⢸⣿⣯⣿⡿⠁⢠⠁⠘⠌⢰⢺⣿⣿⣿⡇⡇⠹⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠽⠿⠧⢸⣿⡿⠗⠀⠠⠀⠃⠀⠀⢸⡇⢻⣿⣿⡞⣿⡆⠌⣿⡛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣼⡿⣻⣷⡿⠻⢾⢿⣻⣾⡟⢳⣿⣿⠡⣽⣿⢱⡟⣛⠈⣿⡿⡜⣿⣷⣸⣿⣷⡽⣿⣷⣝⣿⣿⡛⢿⣬⣟⠿⢮⣿⢹⢛⣙⢿⣿⡽⣿⣿⣿⠿⠟⠛⢛⣛⣛⣛⠛⠛⠛⠛⠛⠛⠋⠂⠘⠛⠛⠛⠛⠛⠃⡆⠘⢿⡇⡄⣤⣿⣿⣯⣼⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣯⠀⠈⣛⣿⣿⣟⣛⣛⠛⠛⠿⠿
⢸⡗⣿⡿⠉⠀⠀⠠⠒⠀⢸⣼⡿⢼⣿⡟⣥⣤⣤⣤⣤⣤⣦⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⡀⠀⠘⠋⠀⠉⠉⠀⠀⣦⢠⡌⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣹⣾⡽⢫⣾⣿⢫⣼⣿⣍⣤⣾⡿⢣⣾⣻⡅⣾⣿⡏⢨⣿⣏⠀⣷⣶⣤⢿⣽⣥⡹⣿⣿⣜⣿⣿⣯⡻⣿⣿⡟⣯⣥⣜⠻⣿⣦⣟⣿⣤⡔⠒⣤⣤⣽⢷⣶⣶⣶⣶⣶⣶⣶⣶⣶⠦⠀⠀⠀⢀⣀⣈⣉⣩⣽⣶⣦⣴⣿⣷⣧⣼⣿⣿⣿⣿⣿⣿⣿⣯⣤⡀⠀⠁⠀⠀⠀⠀⠀⠀⠈⠀⠀⠋⠀⠘⠁⠀⠚⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣾⣷⢸
⢸⡟⠟⠁⠀⠂⠘⠆⢶⡟⢸⣿⢹⢘⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠿⠿⠿⠿⠿⠟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠂⠀⢀⣀⣀⣀⣀⣀⠀⢀⣀⡀⠀⢀⣤⣬⣥⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡏⣴⣶⡟⣯⣾⣿⠟⣽⣿⣿⢃⣬⣭⣥⢠⣼⣷⡖⠘⢿⣿⠟⣴⣿⣿⡒⣹⣶⣯⠈⣿⣿⣷⣸⣿⣿⣎⠻⣿⣿⣎⢭⣽⣶⣴⣦⣶⣌⡛⢾⣿⣦⣰⣾⣛⣂⠘⣳⣶⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣯⡛⡂
⠉⠀⠀⡀⠀⠛⠨⢽⠂⣠⣭⣭⣬⣭⣭⣥⣽⢿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣷⣾⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣧⣟⣾⠗⣠⣶⣶⠞⢉⡚⠿⡿⢱⣶⣶⣒⠀⢼⣿⣿⡇⣸⣛⡒⠲⣶⣭⣥⣄⢿⠿⣿⣯⢻⣿⣿⣇⢲⣾⣶⣶⡹⣿⠿⠗⠐⢷⣶⣶⡝⠿⠿⣶⣬⡛⢓⣶⣖⠫⠭⣤⣄⡚⣿⣿⣿⣿⣿⣿⣿⣿⣛⣛⣛⡛⠛⠛⠛⠛⠛⠋⠉⠉⢭⣥⣤⣤⣴⣤⣀⣀⣀⣄⣀⣀⠀⠀⠀⠂⠀⠈⠋⠉⣽⣿⣿⠟⢛⠛⠛⠿⢿⣿⣿⡿⠀⠀⠀⠘⣟⣛⣛⣟⣿⣿⣿⣫⣤⣤⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿
⠢⠄⠘⠁⠀⢀⠀⠀⠃⣿⣿⣿⣿⣿⣿⣷⢸⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⣸⣿⡟⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣑⣀⡁⡿⠱⠛⢾⠟⠁⣸⣿⣛⠛⣴⣶⣾⡿⢣⣶⣶⡿⠆⢾⣿⣿⡿⠋⣿⠿⠛⢋⣶⣶⣬⣴⡲⣿⣿⣿⣯⢻⡿⠿⠟⠈⢻⣿⣟⣀⡱⣶⣾⣿⣟⢷⣶⣶⡺⡻⣿⣿⣿⣍⠻⠿⠗⠀⠒⣴⣤⣍⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣤⣬⣤⣬⣼⣝⣛⣛⣛⣋⣙⣈⣁⣀⣀⣀⣤⣤⣤⣄⠘⢶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣚⠁⣄⡆⣀⣴⠂⠀⢠⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⣿⣟⡟⠛⠛⠛⣛⣛⣛⣛⣉⣉⣩⣹⣿⣿⣽⣿⣷⣶⣿⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣟⣻⣶⣑⡶⠎⢈⣹⣿⠿⢁⣶⣶⣾⡿⢋⣘⣛⣛⡛⠳⣾⣾⣦⡞⢱⣿⣼⢿⣓⠐⣻⡿⠟⢊⢐⣾⣿⣿⣋⢘⣿⣿⣷⣆⠻⢟⣻⣯⣄⠿⣿⣿⣶⣄⠛⣛⣛⣋⣙⠷⣶⣾⣧⡛⢿⣿⣝⣋⣛⡛⢿⣶⣦⠛⢿⣿⣛⣛⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣈⣋⣙⣙⣉⣉⣉⣉⣛⣛⣛⣛⣛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿
⢡⣷⣾⣧⡐⣠⢠⠀⢸⡿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣫⣴⣴⣲⣿⢟⣀⣺⣿⣻⠏⣐⣿⣿⣿⠟⣀⣙⣙⣛⡛⠡⣒⣒⣲⣶⣦⣾⣛⣳⣿⡖⢠⣔⡲⢾⣿⣆⣿⣴⣶⣂⡴⣾⣿⣿⣿⣂⢿⣿⣿⣿⣦⠙⢻⣿⣿⣷⡈⢙⣛⣛⣃⣀⣲⣒⣒⣒⡿⢿⡿⣞⣛⣶⣆⠴⣿⣷⣶⣮⣻⡶⢦⣼⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣦
⠼⠟⠫⠉⠀⠀⠀⠀⠸⠰⠿⣿⣿⣿⣿⣋⣁⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠶⣝⣻⣿⣿⠟⠵⠿⠿⣿⡿⠛⢝⢿⣿⡿⠋⠺⠿⠿⢿⡿⢋⣾⣿⣿⣷⡎⢀⠹⠿⠾⡿⠅⣾⣿⣏⣐⣶⡅⢶⢮⣽⣻⡷⠙⠯⣛⡿⣿⡏⠻⠿⠿⠿⣦⣍⠻⡟⠿⠿⡆⠙⣿⠿⠿⠿⠾⡻⣿⣷⣶⣦⣅⠉⢛⠿⠦⠸⠿⢿⠶⣎⣑⣀⡺⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟
⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⡿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢏⡶⠿⣾⣿⡿⣉⣷⣶⣶⣶⠤⣠⣴⣾⣿⣷⡟⣥⣼⣶⣶⣶⡠⢁⣾⣿⣿⠿⠿⠡⠭⢯⣤⣔⢦⡤⣤⣄⣛⣋⣉⣁⣿⣷⣿⣿⡿⡙⢷⣿⣿⣭⣵⣕⣶⣶⣾⣿⣗⠺⢻⣶⠾⣽⣷⣎⢽⣶⣶⣦⣤⣬⣿⣿⣿⣛⣁⣰⣷⢶⣶⢶⣦⣤⡍⠿⠿⠿⢁⣀⣨⣳⣿⣟⣫⡍⠙⠉⠉⠛⠛⠿⠛⠛⠉⠹⠿⣿⠿⠿⠿⢿⣿⢟⣿⡉⠛⢿⣿⠿⠻⣿⠿⠿⣿⡿⣿⠿⠯⢹⠷⠖⠛⠝⢍⣩⠋⠛⠿⠟⡛⢛⡙⠛⠋⠛⡉⠉⠉⢩⠀
⣹⣥⣽⣯⣍⣭⡛⠛⠋⣽⣿⠭⠭⠿⠏⢉⣭⣽⠶⢞⡚⠬⠋⠉⠊⠛⠁⠻⠽⠭⠿⠛⣻⠭⠛⠛⠉⠙⠋⠛⠿⠿⠟⢛⣛⢛⣙⣶⡿⢹⣋⣍⠃⣙⣅⠘⢙⣀⡐⠰⠒⠂⡈⠏⡉⠉⠉⠁⣈⡉⡁⠙⠿⣋⣬⣿⣿⣿⡟⢻⡿⠿⠿⠻⠎⣙⣓⣛⣛⣶⠿⠛⠳⠾⠯⠿⢿⣷⡺⣾⣿⣶⣿⡟⠂⣐⡯⡿⡿⢿⣏⣉⢹⣿⠦⢀⡶⢶⠻⣿⣿⣯⡽⢟⡋⢖⣛⣛⣽⣿⣦⠀⢶⣤⣉⠙⠶⠹⣿⡿⣿⣿⣿⣏⣠⠶⠿⠿⠿⠶⢶⡙⣤⣦⣬⣝⣛⣛⣿⣿⣯⠓⢉⣉⣰⣦⣤⣄⠶⠮⢀⡴⠶⠄⡀⠀⠁⠖⠄⠠⠀⠀⠀⠀⠀⠀⠤⠶⢦⡬⠶⠿⠶⢋⡈⠀⠰⠾⠗⢉⢴⣝⣳⠶⠆⣉⣒⣦⣤⣲⣶⡀⢀⣀⣤⣀⣉⣂⣰⠾⠗
⢿⣷⠿⠏⠉⠉⢀⠀⠴⠟⣁⠄⠠⠀⠐⠀⠉⠉⣙⠻⣫⣑⣦⣌⣵⣾⠾⠟⠉⠀⠀⠀⢠⣤⣰⣒⡴⠧⢦⣴⠲⠶⡶⠀⠈⠈⠉⠤⠤⠽⠿⠗⣰⡿⠝⠛⠿⠉⠅⠐⠒⠁⠻⠍⠷⠖⣷⣿⣑⠶⠾⣯⣶⣿⣿⣽⡻⢞⣿⣶⣾⣿⠿⡟⠂⣐⡊⠀⣠⣁⣩⣤⣺⣯⣏⣻⣵⡉⣡⣼⣿⣿⣷⣭⣤⠉⠁⣬⣩⣴⣭⠿⠅⡡⢤⠾⠶⠶⠿⠟⠃⢙⣲⢟⡛⠀⣿⣿⣿⣿⣽⣿⡹⢿⣿⣿⣿⣷⡿⠦⠽⢊⣃⣈⣽⢿⣏⢨⣿⣶⣶⣯⣌⣹⣿⣿⣿⣷⣿⠼⠿⣿⣿⣯⣭⣉⣉⡁⣀⣀⣁⡸⣉⣭⣥⢤⣴⡤⠄⢠⣶⣶⠶⣶⠶⠶⠶⠤⣶⣶⢦⣶⠶⢮⣿⣿⡿⢶⣤⣤⣠⣭⣤⣌⣭⡿⠟⣩⣭⣭⣍⣤⣷⠹⢿⣿⣧⣬⣉⣁⡀
⠯⠭⢤⠆⠤⠐⠈⠑⠀⠚⢷⠾⢛⡃⣀⡀⠚⠋⢉⣠⣬⣭⣷⠬⢥⠠⠒⢶⠶⠾⠋⣻⣛⣩⣭⣹⣉⣁⡔⠿⡌⠈⠉⠉⠙⣙⣹⣒⡮⠭⠥⣭⣵⣲⢒⣉⣐⣷⣾⣿⣿⣋⢀⠰⠾⢯⠿⡯⠭⢥⣤⣭⣭⣩⣭⠍⠐⣒⣎⣭⣍⣁⡀⢴⡾⠿⠷⣯⣹⣿⣯⣿⣿⢯⣯⣙⣏⣻⣽⣽⣿⣽⠿⠟⠃⢤⣍⣙⠿⠋⠉⠆⣰⣿⣮⣭⣭⣴⡾⣾⣯⡟⠯⠯⣽⡾⠏⣭⣭⣭⣭⠉⣥⣴⣿⡯⢉⠭⠩⣤⣤⡿⢿⡿⠁⠻⠿⠷⢮⠿⣿⣿⣿⣟⣻⣭⠿⣿⡿⠿⣷⠶⠶⢍⠛⠛⠯⠅⠉⠉⠿⣿⣯⣭⣤⣤⡿⣿⠿⣤⣭⣍⣥⣤⠥⣬⣤⣴⡾⠿⠾⠍⢳⣾⣭⢽⣋⡙⠉⠉⠻⣿⣿⣿⣿⣯⣥⡿⣿⣿⣶⠯⣴⠬⢭⣽⠯⠽⡭⢭⡅
⣴⣦⣿⡗⠂⠐⠋⠉⠠⣶⣶⡿⣿⣟⣝⣟⠛⠿⠿⡛⠉⠁⠹⣿⡛⠓⠛⠩⠿⠌⠉⠋⣁⠀⢀⣀⠈⡰⢿⣿⣿⣯⣿⣿⣭⣿⣿⠟⣯⣿⣿⡉⣻⣥⣾⣝⣭⣭⣽⡛⢛⢉⣭⣿⣿⡟⠛⢋⣑⣊⣙⣯⣿⠷⠉⠠⣬⣭⣽⣯⣭⣿⡄⢠⣄⣶⠻⡋⠋⠲⢶⣬⠁⠬⠿⢿⠟⢡⣽⠷⣶⣯⣿⢟⣋⣽⠿⣿⣻⣛⣛⣬⡛⣯⣍⣫⣭⣁⠐⣄⣐⣛⣿⡿⢿⡛⠷⠮⠟⠁⣩⣤⣤⣌⠉⠚⣟⣉⢁⣀⣀⣭⢀⣴⣶⣄⣽⣿⣷⣌⡙⢿⣿⡿⠿⢿⠭⣤⡠⣴⣿⣿⣿⢿⣿⡟⠲⣶⣶⣶⣶⣮⣬⣽⢿⣿⣿⣷⣍⣡⣤⣬⣭⣽⣧⣍⣭⣭⠍⢿⣿⠿⠷⢭⠉⢔⡭⡭⠹⠟⠂⢹⡗⢾⠶⡶⠢⠚⡻⠿⠷⠟⠛⠛⠉⠁⣠⡴⠼⡿⠇
⣾⡿⠒⣀⡀⡠⠠⠀⠤⠬⠍⣡⣿⢟⣭⣴⢶⣾⣅⣿⣿⣿⠟⢛⠿⠛⠛⠇⣐⣾⣢⠐⢾⣿⣷⣶⣴⡿⢿⣿⡶⣶⣦⣄⣙⣭⣴⣶⣴⣾⣿⣷⣮⣽⣟⠛⠻⣣⡖⢲⡿⣿⣿⠿⣫⣷⣾⣻⣿⣿⣟⠿⣬⣿⣻⣖⢣⣮⣥⢀⠰⠛⠚⠻⠿⠛⠛⠿⣉⣻⣏⣛⠩⢠⠶⠧⠈⣽⣟⡛⠻⠿⠿⠷⢰⣿⠿⢿⣿⣿⣦⣽⣙⠾⠶⠶⢾⣿⣿⣯⣽⣿⣤⣤⣄⣤⣤⣤⣾⠿⠟⠛⠛⠿⠟⢀⢸⣿⣿⣷⣴⡿⣦⡍⠛⢿⣿⠿⠿⠟⠻⠷⠺⠷⣟⣉⣀⣀⡸⣮⣻⠏⣰⣾⡛⣛⣻⡉⣿⡿⠿⢿⣿⣤⢤⣟⠚⠻⣿⣿⣿⣿⣯⣵⡅⠤⠉⠱⠛⠃⠐⠬⠁⠤⠤⠸⣤⣦⣤⠄⢰⣾⠷⠿⠧⠍⠟⠿⣦⣤⣶⣾⣿⣦⣴⣾⣤⡾⠿⠿⠇
⢩⡄⣠⣤⢶⣶⠠⠄⠲⣾⡿⢿⣿⣯⡝⣿⣿⡙⢯⣭⡅⢤⣤⣤⣼⠿⠈⣿⣿⠿⠿⣿⣿⠓⠀⢨⣭⣿⠛⡿⠿⠷⢶⡶⢿⣷⣶⣾⣓⡎⠙⣩⣃⣤⡄⣀⣾⣥⢶⣶⣿⣿⠗⠠⣶⡆⣾⠿⣿⣿⡿⠷⢛⣭⣭⣭⣽⣿⣷⢲⣯⣿⣿⣿⣿⣿⣿⡁⠿⣿⣿⣿⡿⣿⣿⠛⣥⣿⣿⣿⡿⢟⡷⡓⠮⣻⣿⣿⣿⠯⢳⣮⠛⣭⣴⣿⣿⣶⣶⣶⡆⢀⣻⣷⣾⣷⣯⣿⡆⠰⣾⣿⣍⣛⠿⣿⢷⡈⣿⣿⣍⣩⣭⣿⣥⣤⠙⢿⣶⣶⣶⣶⣶⣀⣘⡻⣿⣿⣿⡿⢷⣤⣍⣿⣿⣯⣿⠿⠳⡶⣿⡷⠺⢿⣿⣿⣷⣶⣾⡿⣿⣷⣾⣷⣶⣾⣶⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣶⣶⣿⣃⣀⣀⣀⣀⣀⣤⣨⣷⣾⣮⣿⣯⣼⣿⣿⣿⣷⣼⣿⣭⣤⣤⣤⣤⣤⣬⣿⣿⣿⣿⣿⣿⣿⣿⣤⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⡟⢻⣿⣟⢻⣿⣷⣾⡻⡟⠋⣠⣤⣶⣤⣽⣷⣶⠄⣴⣾⣿⣿⢟⣉⣛⠓⠀⢤⣊⣿⣿⡿⣿⣿⡿⠂⢀⣀⣅⣘⣋⣩⣤⣤⣥⣼⣿⣟⣿⠧⠶⡮⠳⢤⣬⣽⣭⣩⣤⣤⣤⣤⡸⠿⣿⣿⣯⣤⣿⠛⠈⠻⢿⣿⢛⣿⣿⣿⡦⠨⣵⣾⣮⣿⣶⣶⣤⡀⢹⣿⣿⣳⣯⣉⣚⣻⡀⠛⣿⣿⣿⣿⣿⣿⣤⣤⢡⣤⣼⣯⣭⣥⣼⣮⣻⣿⣿⣯⣶⣾⣿⡆⠤⡬⠙⣯⣤⣤⣤⣤⣼⣟⠟⡏⢿⣤⣽⣟⠿⠛⡛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠠⡶⠶⣶⣶⣶⣾⣿⣿⣤⣾⣷⣿⣥⣞⣓⣉⣃⣘⡛⠿⠛⠛⠛⠿⠛⠘⠛⠻⠛⠿⠿⢿⣿⡟⢃⣴⣿⣿⣿⣿⣿⣿⣿⠗⢀⢖⣢⣼⣟⣿⣶⣦⡀⢀⡀⣤⣤⣤⣶⣶⣦⣍⢴⣾⣖⡾⠿⠿⣓⣂⢤⣴⢶⣶⣶⣶⣶⣶⣿⣶⣼⣿⣿⣿⣶⣿⣟⣭⣤⡈⠛⡿⣟⣛⣛⣛⡛⠂⠈⠛⠛⠛⠛⠿⠿⢿⣮⣿⣿⣿⣿⣻⣿⣷⣲⣶⡦⠠⣶⣞⣀⣴⣿⣿⣷⣦⡄⢀⣀⣠⣤⣤⣤⣄⡶⣤⡚⢷⣿⡿⠟⣚⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣛⢷⣿⣿⣿⣿⣽⡻⠻⢿⣟⣛⣿⣿⣿⣿⣿⡓⠁⠘⣿⣿⠻⢾⢿⣿⢿⡃⢀⣠⣀⣤⣄⣠⣄⡲⡆⠀⣛⣥⣉⣁⣈⣫⣍⣛⠆⢐⣛⣛⣛⣛⣻⠯⣟⠋⠁⣒⣯⣶⡖⢿⡶⣛⣷⠛⠰⢶⡶⠾⠛⠛⠻⣿⡓⢮⣿⣿⣿⣻⣭⣛⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡃⠀⠉⠛⣿⠟⠿⠿⠿⡿⠇⠐⣶⣖⣤⣄⣐⣒⣪⣉⡑⢋⣤⣉⣉⣉⣭⣙⣃⣘⠛⡻⣟⣛⣋⣀⡫⣼⣯⡈⠹⣵⣖⣒⠲⠞⡻⠟⠀⣒⡺⢽⠛⠿⠛⠛⠻⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿''',0.5)
def necrofight_art():
    echo('''⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿⢹⣦⡙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⢧⠀⠀⠀⢿⠀⢂⠀⠀⠀⠀⢸⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⣾⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢸⡇⠘⡄⠀⠀⠈⠀⠈⠀⠀⠀⠀⣾⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⢺⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢁⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡛⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⢀⣄⠈⠋⠉⠉⠉⠀⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣌⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣡⠸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡿⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⢻⡄⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣇⢻⣧⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣾⠃⠙⡁⠠⣤⣄⣀⣀⣀⣀⠀⣀⣀⣀⣀⣀
⠀⠀⠀⠀⠀⠀⠀⠀⠐⠂⠀⠐⠒⠚⠁⣾⡻⣿⣦⡁⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣌⠹⣾⣿⠇⠀⠀⠀⠀⠈⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⠄⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠟⠁⠰⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡌⢠⠀⠡⣶⡀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠖⠁⠀⠘⠠⠃⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀
⠶⠶⠶⠶⣶⠶⣶⠶⠶⠀⠀⠀⠀⠀⠀⣌⠠⣁⠀⠈⠹⢶⠈⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠊⢰⡃⠀⠀⠀⠀⠀⠉⠛⠻⠛⡟⠉⠙
⠀⠀⠠⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣌⠀⠀⠀⠀⠑⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣴⣶⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠆⠀⠀⠀⠀⠀⡇⢸⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣶⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡶⠿⠿⣿⣋⣉⠉⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠢⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢠⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠻⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣀⣠⣴⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣷⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⢸⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠴⠆⠀⠘⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣄⠻⣿⣿⣿⣿⣿⣿⠿⠿⠃⠀⠀⠀⠀⢀⣀⣀⣠⣤⣤⣴⣶⣿⣿⣿⣶⣶⣤⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⡈⠉⠯⠿⠷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠼⠊⠉⠀⠀⠀⠀⠀⠀⠀⠀⢠⠖⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡄⠛⠛⠋⢉⣀⣐⣠⣭⣤⣶⣶⣶⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣹⣿⣿⣿⣿⣿⣿⣷⣶⣶⣤⣤⣤⣀⣀⣀⠀⠀⠀⠀⠈⢻⣿⣷⣶⣤⡀⠀⠉⢻⡄⠀⡀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠿⠛⠁⣠⣶⣶⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⢿⣿⣿⣿⣿⣦⣤⡾⢁⣼⡿⢦⣄⠀⠀⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⣯⣾⣿⣿⣿⣿⣾⠿⣿⣿⣻⣿⣿⣿⣯⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣕⠪⢙⠻⣿⣿⡟⢡⣾⣷⡀⠀⠉⠛⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⡀⠀⠀⠀⠀⠀⠀⠀⣀⠆⠀⠀⣠⣶⠟⠁⠀⡀⠀⠀⠀⠀⠀⠀⡀⠀⣨⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢋⣥⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣾⣿⣮⣍⣛⡿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣕⠢⣍⠰⣿⣿⣿⣿⣶⣄⠀⠀⠹⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⣄⠀⠙⠦⡀⠀⠀⠀⢠⡾⠋⠀⣠⣾⠋⠀⢀⣾⣿⡟⠀⠀⠀⠀⠀⣨⣴⣿⣿⣿⣿⣿⣿⡿⠋⣿⣴⣿⣿⠏⣾⣿⣿⡿⠶⠟⠛⢛⠛⣛⣡⣭⡴⣶⣶⣶⠶⣶⣶⣴⣶⣶⣶⣶⣦⣭⣙⣛⣛⠛⠛⠿⣷⣮⣝⡛⠿⣷⣶⣦⣝⣿⣿⣿⣿⣿⣿⣿⣷⣦⣕⠢⣙⠻⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠄⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠁⠀⠀⠀⠀⢀⡿⠈⠀⣠⣦⡈⠻⣷⣾⣿⣿⣿⠇⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣏⡴⡿⠿⣻⣯⣵⡾⠿⢛⣩⡖⣴⣿⠘⡿⠹⣿⣿⠏⠄⣿⣿⡇⠾⣼⣿⣿⡎⣿⣿⣏⠿⣿⣿⡯⣹⡏⢹⣿⡆⣦⣝⡻⠷⣶⣭⣛⣻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣅⠂⡙⢿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠘⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⢸⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⢠⣼⠏⠀⢙⣦⡈⠿⡿⠟⠡⣂⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣯⣥⣾⠟⠛⣉⣤⣶⣿⣯⡻⠃⢿⣿⠀⡇⢀⣿⣿⠀⠀⣿⣿⡇⡄⣿⣿⣿⡇⣿⣿⣿⠀⣿⣿⡇⢹⡇⢸⣿⠃⠟⣫⣿⣷⣶⣌⣙⠻⠿⣦⣝⡻⢿⣿⣾⣟⣿⣿⣿⣿⣿⣿⣦⣄⠈⠻⠟⣀⠀⠀⠀⠀⠀⢠⡀⠀⠙⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐
⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣸⣿⣿⣗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠞⠁⢀⣴⠋⠁⢀⣴⣿⣿⡿⠂⣠⣴⣾⣿⣿⣿⣿⣿⡿⣻⣿⣿⢟⣫⣴⠟⢋⣥⣖⠿⣿⣦⡠⡉⠻⢿⣿⣦⣾⡟⢿⡇⢸⣿⣿⠀⢸⣿⣿⡇⠇⣿⣿⣇⠇⣿⣿⣿⠀⣿⣿⣷⠸⡧⢜⣿⣶⣿⡿⠟⠋⡡⢠⣾⡿⢀⣶⣌⠻⣶⣭⣛⢿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣦⡀⠙⠀⠀⠀⠀⠀⠀⢹⣦⡀⠈⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⠀⠀⠀⠀⢀⡰⠃⠀⣠⣿⠇⠀⣰⣿⣿⣿⠏⠀⣼⣿⣿⣿⣿⣿⣿⠟⣡⣾⡟⢫⣵⠿⣛⢱⣿⡀⢿⣿⣆⢈⠻⢿⣮⣓⠦⣨⡙⠿⣿⣷⣅⢸⣿⣿⡆⠸⣿⣿⡇⡀⣿⣿⡟⠀⣿⣿⣿⠀⣯⢹⣿⠀⣰⣾⡿⢋⠁⠠⢒⣩⣶⡿⢋⢀⣾⣿⠃⣼⣦⢉⡻⢷⣯⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⢀⠀⠀⠙⣷⣄⠀⠙⣦⠀⠀⠀⠀⠀⠀⠀⠀⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡂⠠⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⣼⣿⣫⣴⣾⣿⣿⡿⠁⢢⣾⣿⣿⣿⣿⣿⣿⣿⣿⢏⣭⡾⢛⣵⣾⣏⠘⣿⣇⠀⢻⣿⡄⠳⢌⠻⢿⣷⡈⣿⣷⠈⢿⣿⣶⡍⢿⡇⠀⣿⣿⡇⡇⣿⣿⠅⠀⣿⣿⡿⠈⣿⡆⣡⣾⡿⠋⡤⣿⡧⣴⣿⠿⢋⠴⣣⣾⣿⠁⣌⣿⡏⢠⡿⣠⡍⠻⣮⡛⢿⣿⣿⣿⣿⣿⣿⣿⣷⡀⡀⢄⠀⢻⣧⡀⣀⡿⠃⡀⠈⢷⣄⠀⠀⠀⠀⠀⠀⠀⠙⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣦⡀⠀⠀⠀⢀⣠⠏⠀⣠⠦⣌⠙⠿⣿⣿⣿⠏⠐⣠⣿⣿⣿⣿⣿⣿⣿⣿⠿⣣⣿⢋⣤⡘⢿⣿⡌⢂⠙⣿⡆⡄⢿⣿⢸⣦⡑⢄⠛⡿⢿⣿⡰⡀⠛⣿⣿⡌⣷⡆⠻⣿⡇⠇⣿⣿⣄⠀⣿⡟⠀⣠⡿⢰⣿⠏⠀⢰⢃⣿⡿⠛⠋⠤⣫⣾⣿⣿⠋⡸⣸⡿⠀⠜⣴⣿⠋⣰⣌⠻⣦⡙⢿⣿⣿⣿⣿⣿⣿⣿⣄⢊⢀⣘⡿⠟⢉⣴⣾⣷⡀⠀⠻⣄⠀⠀⠀⠀⣠⠴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⢰⣿⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡞⠀⠀⠀⢀⠉⠀⠀⠀⣾⠋⠀⣰⠏⠀⢘⣿⣶⣌⠙⢋⢈⣶⣿⣿⣿⣿⣿⣿⣿⡿⣋⠸⢟⣁⠺⣿⡇⠈⢻⣿⣎⠀⣿⣷⣣⠈⣿⣧⠹⣿⣦⡃⡀⢸⣿⣷⣷⠀⠛⢿⣇⢸⣿⠀⣿⣧⠃⣿⢻⣿⠀⣿⡇⠀⣿⢠⣿⡏⠀⢠⣿⣿⣿⡇⠀⣠⣾⡿⢋⣼⡟⢀⣇⣿⡇⢀⣾⡿⠁⠠⣠⡾⠀⠙⢿⣦⡛⢿⣿⣿⣿⣿⣿⣿⣦⠢⡁⣤⣾⣿⣇⠀⠉⠻⣄⠀⠙⣇⠀⠀⠀⠀⠀⠀⠀⠀⢢⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⠀⢸⣿⣿⣿⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠃⠀⠀⠀⠀⠀⠀⠀⣾⠃⠀⣴⠋⠀⢀⣾⣿⣿⡟⠑⢠⣾⣿⣿⣿⣿⣿⢟⡉⣥⣾⢟⡀⠸⣿⣆⠹⣷⡅⠀⠙⢿⣷⡼⢿⣯⡆⢸⣿⡔⠈⠻⣿⣄⠘⣿⣿⣿⡇⠈⠞⣿⡄⢿⡄⢸⣿⠀⠟⠀⢿⢰⣿⡇⢰⡏⣼⣿⠀⠀⣼⣿⣿⣿⢀⣦⣿⠋⠀⣸⣿⠁⣸⣿⠿⣠⣾⠟⠁⠀⣱⡿⢁⣼⡍⠀⠉⢿⣦⡙⣿⣿⣿⣿⣿⣿⣷⡐⡘⢿⣿⣿⣄⠀⠀⠹⣆⠀⠹⣦⠀⠀⠀⠀⠀⠀⠀⠈⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⢸⣿⣿⣿⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠
⡀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠏⠀⣼⠃⠀⢠⣿⣿⣿⠟⠐⣰⣿⣿⣿⣿⣿⣿⡿⢊⣾⡟⢱⣿⢷⡀⠘⣿⣷⡹⣷⡄⡀⠈⠹⢿⣶⡙⣿⠈⣿⣷⢰⠀⠙⢿⡇⣿⣿⣿⣿⠀⠈⢻⣷⠸⣧⠀⣿⣆⠀⣆⠈⣸⣿⠀⣿⢠⣿⡇⠀⢠⡿⢸⣿⡇⢼⠟⠁⢀⡆⣿⡟⢀⡟⣫⣾⡿⠋⠀⠀⣼⡿⢡⣿⠋⠀⣠⣏⣦⠙⣿⣌⢿⣿⣿⣿⣿⣿⣿⣌⠈⢿⣿⣿⣆⠀⠀⠻⣆⠀⢻⣦⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⢸⣿⣿⣿⠂⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠
⡇⠀⠀⠀⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⣴⡏⠀⣰⡇⠀⢀⣿⣿⣿⠇⢀⣼⣿⣿⣿⣿⣿⣿⡟⣴⡟⠉⣦⡈⢻⣿⣷⣄⠘⣿⣷⡘⣿⣷⡀⢳⣦⡙⠿⣧⣄⢹⣿⢨⣷⣄⠀⠁⢸⣿⣿⣿⡇⢀⢸⣿⡆⢱⡆⢻⣿⡀⣿⢠⣿⡟⣸⡆⢸⣿⡇⠀⢸⡇⣾⣿⡇⠠⢀⣴⣿⠇⢿⠃⡀⡾⠟⢉⣴⠀⢀⣼⡟⣱⣿⠃⠀⣼⣣⣿⠋⣴⡆⠹⣦⡹⣿⣿⣿⣿⣿⣿⣆⠀⢻⣿⣿⣆⠀⠀⠹⣆⠀⢻⣆⠀⠀⠀⠀⠀⠀⠀⠈⠅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠈
⠃⠀⠘⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣿⣿⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠻⠤⢠⣾⣿⣿⠃⢠⣾⣿⣿⣿⣿⣿⣿⠟⣵⡿⣡⡀⠻⣿⡤⡹⢿⣿⣠⠘⣿⣧⡈⢿⣿⡀⢿⣧⠢⠀⠈⢸⡿⣶⣭⣍⡁⢀⢸⣿⢿⣿⣷⠸⢸⣿⡇⣼⡇⠸⣿⡇⣿⢸⣿⠀⢿⣧⢸⡿⠀⠀⣿⡇⣿⣿⡇⠠⢚⣉⣡⠴⢿⠀⠀⠀⢆⣾⡏⣠⣿⠏⢰⣿⡏⠀⢠⣾⠟⠁⣴⣿⠀⣴⡙⣷⡜⣿⣿⣿⣿⣿⣿⣧⡀⠹⣿⣿⡧⠚⠋⣡⡄⠀⢿⡆⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⢸⣿⣿⣿⡇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀
⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣿⣿⠀⢸⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⠀⠀⢠⡿⠀⢠⡿⠳⠦⣤⣉⠛⠃⣰⣿⣿⣿⣿⣿⣿⡿⢁⣾⠏⣼⣿⣿⠀⢻⣿⣿⢈⠻⣿⣆⠘⣿⡇⢦⡙⢿⡜⣿⣇⢣⠀⢸⣧⠀⣄⡉⠛⢶⣬⡛⢼⣿⣿⡄⢸⣿⡇⣿⡇⡆⢿⣷⠉⣼⡟⢠⢸⣿⢸⣿⡀⠀⣿⣷⡯⢛⣥⡶⠛⣁⡀⠀⣸⡄⠀⠌⣼⣿⠱⠛⢁⠔⣸⡿⠀⢰⡿⠃⡰⣸⡿⠁⢠⣿⣿⠘⢿⣎⢻⣿⣿⣿⣿⣿⣿⡄⠉⣤⣴⣞⠋⠉⢳⡀⠈⢿⡀⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
⠀⠀⢀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣿⣿⡇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⢄⣀⠀⠀⠀⠀⠀⣾⠃⠀⡿⠁⠀⢀⣿⣿⠇⢰⣿⣿⣿⣿⣿⣿⡟⢡⣾⠃⣀⣛⣛⣿⣤⡀⢻⣿⣾⣦⡹⡏⠀⣿⣇⢘⣛⠦⣀⠈⠿⣷⡄⢸⣿⢠⡘⢿⣷⡦⡘⢻⣦⡝⢿⠇⣼⣿⠀⣿⣇⢳⠘⣿⣄⣿⠁⡾⢸⣿⠘⣿⣇⠀⣿⢋⣴⠟⠁⢀⣾⠿⢀⣼⣿⡇⢠⣾⠟⠁⠀⠔⢋⠀⣿⡇⠀⡤⢀⠌⣰⡿⠁⣰⣿⠿⣛⣃⡈⣿⡌⢿⣿⣿⣿⣿⣿⣿⡄⢹⣿⣿⡀⠀⠀⢳⠀⠘⣧⠀⠀⠀⠀⠀⣀⡤⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⣠⠀⠀⡇⠀⢸⣿⣿⣿⠅⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄
⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣿⣿⡇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⡄⠀⠀⠉⠀⠀⠀⣼⠏⠀⡼⠁⠀⢀⣾⣿⡟⠀⣼⣿⣿⣿⣿⣿⣿⢁⣾⠏⣘⢛⠻⠿⣿⣧⣅⢸⣿⣿⣿⣇⠌⠀⢸⣿⡎⢻⣿⣶⣗⡤⠀⠀⢸⣿⢰⣅⠀⠘⠻⣷⣈⠻⣿⡌⣰⡟⠃⣤⢹⣿⡘⠀⢹⣿⡇⢰⢣⣿⡇⢰⠙⢻⣆⢠⡾⠃⣠⣴⠟⠃⡠⣲⡿⣹⠆⠀⠀⢀⣠⣶⣿⠟⢸⣿⠁⠀⠰⣱⢸⣿⡇⢀⣭⣶⡿⠿⠛⠃⠘⣿⡘⣿⣿⣿⣿⣿⣿⡇⠈⣿⣿⣧⠀⠀⠀⡆⠀⢹⡇⠀⠀⠒⠉⠁⠀⣠⠔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⣼⣿⣿⣿⠅⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣿⣿⡇⢨⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠀⢰⠇⠀⠀⣼⣿⣿⠁⢰⣿⣿⣿⣿⣿⣿⡏⣼⡏⠐⣿⣶⣔⡂⢤⣉⠛⠀⢿⣿⠹⣿⣦⡀⠈⣿⣿⡴⡈⠻⢿⣿⡜⠄⠈⣿⣆⠻⣧⡀⠰⣭⡛⠗⢈⣴⠏⣤⡜⢿⡈⣿⣧⢧⢸⣿⡇⠐⣸⣿⢁⡿⢱⡆⠹⣦⠀⡾⢟⣡⠀⠀⣼⠟⣰⡿⠀⠀⠀⣼⡿⠋⢀⢀⣿⡇⠀⢀⣴⡿⢸⣿⠇⠘⠋⡁⡤⢒⣬⣾⡇⠸⣷⡸⣿⣿⣿⣿⣿⣿⠀⢹⣿⣿⣇⠀⠀⢻⡀⠀⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⣿⣿⣿⣿⡀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⠀⢸⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣿⣿⣿⣿⡇⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⣾⠁⠀⣾⡀⠀⣰⣿⣿⡟⠈⣼⣿⣿⣿⣿⣿⡟⢰⡿⢡⣦⠈⠛⢿⣿⣷⣶⣮⣥⣬⣟⣑⣊⣙⡛⠆⠸⣿⣧⠁⡀⠘⢽⣿⣎⢀⠹⣿⣆⠘⣷⡄⠸⣿⠀⣸⡏⣀⠙⢿⣎⢣⠸⣿⢸⠈⣿⠁⢠⣿⡇⡸⢡⡾⠁⣤⣽⣇⠀⣿⠇⢀⣾⠃⣠⡿⠃⠀⣡⣾⠋⠀⠀⠄⣾⣿⠀⠰⠛⢋⡀⢊⣛⣤⣤⣵⣶⣾⡿⠛⠁⢀⣦⡹⣷⠘⣿⣿⣿⣿⣿⡇⠈⣿⣿⣿⡀⠀⠻⣇⠀⢸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⡄⣿⣿⣿⣿⠀⣿⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⡅
⠀⠀⢸⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢸⣿⣿⣿⣿⡇⢸⡆⠀⠀⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⢰⣿⠀⠐⠛⠲⠶⢿⣿⣿⠃⢠⣿⣿⣿⣿⣿⣿⢡⡿⠁⣛⠿⠷⢶⡦⠤⠉⠛⠛⠛⠛⠻⠿⡟⠻⠿⠿⠄⠻⣿⣧⡑⢄⠀⠙⣿⣧⢠⠘⢿⣷⣜⣛⢢⣻⠀⣿⡆⣿⣧⡈⣿⡇⠀⣿⡇⠀⣿⠀⣿⣿⠁⢠⡟⠀⣼⣿⡇⣿⡆⠟⠐⠛⣣⣶⠟⠀⡠⢰⡿⠁⠀⡠⢃⣼⡿⠇⠀⠿⠿⠿⠿⠿⠟⠛⠛⠛⠋⠀⠤⠴⠶⠿⠟⣁⢹⣧⢻⣿⣿⣿⣿⣿⢀⢸⡿⠿⠓⠀⣀⣉⡄⠀⣿⡀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠄⠀⣇⡇⣿⣿⣿⣿⠀⣿⠀⠀⠀⠀⣽⠀⠀⠀⠀⠀⠀⡇
⠀⠀⠈⡀⠀⠀⠀⠀⠀⣦⠀⠀⠀⠀⣿⢸⣿⣿⣿⣿⡇⢸⡇⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⣸⡇⠀⠿⠓⠲⣶⣶⣦⣍⠈⢸⣿⣿⣿⣿⣿⡇⣿⡇⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣷⢰⣾⣶⢠⣤⣄⡒⠠⣄⠈⠻⣿⣎⡗⣄⠹⣿⣦⠱⣄⠙⠻⢿⣿⡄⢀⣿⡆⣿⣯⣥⠘⣿⠀⣿⡇⠀⠿⢀⣿⣿⠀⢸⡇⣬⣽⣿⠁⣿⠃⢠⣥⠾⠋⠁⣠⣾⢀⡾⠁⣀⠞⣣⣿⠟⠁⣀⠐⣒⣠⣤⡤⣴⡶⢪⣶⣶⣶⣿⣿⣿⣿⣿⠿⠟⠈⣿⡜⣿⣿⣿⣿⣿⡌⠀⣶⣾⣿⡛⠿⢿⡇⠀⢿⡇⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⣿⡇⣿⣿⣿⣷⠁⣿⠀⠀⠀⠀⠿⠀⠀⠀⠀⠀⠃⠃
⠆⠀⠀⠆⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⣿⢸⣿⣜⢿⢟⡇⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⢀⣼⠃⠀⣿⠃⠀⣿⣿⣿⡇⠆⣿⣿⣿⣿⣿⣿⢁⣿⢃⠻⣷⣖⣒⠒⠢⠭⣥⣐⡲⢷⡆⢻⣿⡎⠙⠻⢿⣿⣶⣕⠀⡈⠻⣷⣮⣒⡘⢻⣧⢹⣿⣦⡐⣾⣀⡈⢻⡇⠈⠛⠟⢀⡟⣰⡈⠁⠀⠘⠎⢻⣿⣄⢸⡇⠻⠋⠁⢠⡇⠀⣤⣶⠂⠰⣾⣿⣷⡟⢀⡞⣡⣾⠟⠁⡄⣤⣶⣿⠿⠛⢉⢠⣿⠃⣴⠿⢒⣛⡩⠭⠅⠀⣒⣢⣵⠃⢹⣇⢹⣿⣿⣿⣿⣇⢀⢿⣿⣿⡇⠀⠸⣿⠀⠸⣯⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⢿⣿⠀⣿⡆⠀⠀⠀⣠⠀⠀⠀⠀⠀⠨⠀
⠀⡄⠀⢰⠀⠀⠀⠀⢰⣇⠀⠀⠀⠀⣿⢸⣿⣿⣸⢺⣾⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⢸⠇⠀⠀⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⠏⣼⡇⣜⣓⡨⠉⠛⠛⠿⢿⣶⣶⣮⣍⡒⠄⠹⣿⣮⣓⠤⠌⠉⣉⣤⣾⣷⣮⡙⠻⠿⢷⣿⣥⣯⣿⣿⣶⣶⣅⠈⢿⡆⣿⡇⣾⡇⠘⠃⡀⠀⠈⠀⠈⢿⠏⢸⣷⠸⡿⠀⡾⠁⢈⣉⣩⣬⣭⣭⣭⡭⠶⠾⢞⣋⣥⣶⣶⣤⣉⠉⠀⠔⢂⣵⡿⠃⠠⢒⣨⣭⣶⣾⡿⠿⠛⠋⠉⢅⣂⡈⣿⡆⣿⣿⣿⣿⣿⡀⢸⣿⣿⣿⠀⠀⢹⡄⠀⣿⡆⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⢸⣿⠀⣿⡇⠀⠀⠀⣿⠀⠀⠀⠀⠀⡄⠀
⠀⣇⠀⠘⡄⠀⠀⠀⢠⡁⠀⠀⠀⠀⣿⢸⣿⣿⢹⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠒⠒⠄⠀⢸⡿⠀⣸⡄⠀⠀⣿⣿⡿⠀⣾⣿⣿⣿⣿⣿⢂⣿⢁⠻⠟⠿⠿⣿⣿⣷⣶⣦⣍⢙⠿⢿⣿⣶⣬⡹⠟⢀⣴⣿⡿⠟⣋⣩⣭⣥⣤⣴⣄⡰⣶⣦⡦⢤⣤⣭⣙⡿⡞⢷⣬⣤⣽⡇⠀⡾⠟⠻⠟⠿⠄⠀⢸⣿⣿⣤⣀⡼⠃⢘⡋⣡⡤⣴⠦⣠⣶⠀⣠⣤⣤⣬⣭⣉⣙⠿⣿⣷⣤⡀⠿⢏⣠⣶⣿⡿⠿⠛⣉⣥⣶⣶⣶⠾⠿⠿⠿⠃⢉⡁⣿⣿⣿⣿⣿⣇⠘⣿⣿⣿⠄⠀⢸⡇⠀⣿⡇⠀⠤⠶⠖⠚⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⢸⣿⠄⣿⡇⠀⠀⠀⢽⠀⠀⠀⠀⠀⡇⠀
⢸⠘⠀⠀⡇⠀⠀⠀⠸⣷⠀⠀⠀⠀⣿⢸⣿⢻⣿⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⢸⡇⠀⣿⠀⠀⢠⣿⣿⡇⢠⣿⣿⣧⣿⣿⣿⢹⣿⠘⢿⣦⣤⣔⣀⡈⢉⠉⠻⣿⣿⣦⣶⢬⣭⠍⠀⣰⣿⢛⣉⠶⣿⣶⣶⣿⣿⣿⣿⣭⣿⠤⣹⣵⡿⠛⣩⣤⠤⠤⠄⢈⡙⠿⠇⠰⣟⣉⡇⣿⣙⣓⠀⢸⣿⡿⢋⡁⠠⠤⠬⠧⢈⠛⠷⣦⣭⠀⣼⣿⣯⣭⣯⣥⣤⣴⣶⡶⠉⠛⣿⣆⢀⠉⣭⡥⢀⣴⣾⠿⠛⠉⠉⠁⣀⣠⣤⣶⠆⣸⣇⢿⣿⣿⣿⣿⣿⠀⢿⣿⣿⠀⠀⢸⡇⠀⣿⡇⠀⠀⠀⠀⠀⠀⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⢸⣿⡁⣿⡇⠀⠀⠀⠙⠀⠀⠀⠀⠸⠀⢰
⢸⠀⠃⠀⠁⠀⠀⠀⢰⠇⠀⠀⠀⠀⣿⢸⣿⢸⣿⣿⣿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇⠀⣿⣠⣠⣿⣿⣿⠃⢸⣿⣿⣿⣿⣿⣿⣘⣿⢠⣶⣆⠨⢉⠛⠻⣷⣦⣔⠤⡙⢿⣿⡎⠀⢀⣼⠿⢣⡈⢿⣧⡠⣍⠙⠻⠿⣿⣛⠋⢁⣼⡿⠃⢀⣀⣽⡿⠟⠛⠛⠿⣿⠃⣄⠀⠛⠽⠧⠏⠝⠋⠀⡈⠋⣶⣿⠿⠛⠛⡛⢛⣂⣀⡀⠈⠻⣦⡀⠐⣚⣻⣿⠟⠛⢉⢀⣼⡟⣀⡹⣿⣦⡁⡈⢰⣿⠟⠁⠀⣨⣴⡾⠟⠛⠉⠁⣀⣘⢻⣿⣾⣿⣿⣿⣿⣿⡇⢸⠿⠿⠧⠦⠼⠇⠀⣿⡇⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣼⣿⡃⣿⡇⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠘
⢸⠀⠰⠀⠀⠀⠀⠀⢰⡀⠀⠀⠀⠐⣿⢸⣿⣾⣿⣿⡏⢸⡇⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⣾⡇⠀⣤⡤⠤⢴⣶⣶⡄⢸⣿⣿⡿⣿⣿⣿⣿⣿⠀⠙⠻⢿⣷⣦⣑⠦⣉⠛⠿⠮⠦⢈⣠⣴⡿⠋⢰⣷⣬⣤⣝⢿⣮⣙⢳⣶⠟⠁⣰⠿⠃⣠⣴⡿⠛⠭⠴⢲⣿⣿⡿⠀⣸⣷⡇⠀⣈⡉⢛⠑⠀⣿⣿⡇⢫⣵⠾⢿⣿⣶⠆⠈⠛⠿⣧⣀⠈⢻⣆⠈⢻⣿⠖⣋⣴⣿⣫⣤⣭⣷⣆⠙⣷⣧⣈⠁⢠⡐⠿⠛⣉⠄⣢⣴⣶⡿⠟⠋⢸⣿⣿⣿⣿⣿⣿⣿⠃⢰⣶⣶⡖⠶⢶⡆⠀⣿⡇⠀⠀⠀⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⣿⡇⣿⣿⣺⣟⠃⣿⡇⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⡆
⠈⡆⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⢀⣿⢸⣿⣿⣿⣿⡇⢸⡗⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡎⠀⠀⠀⠀⠀⢀⣿⡇⠀⣿⠀⠀⢸⣿⣿⡇⠸⣿⣿⣷⡝⣿⣟⢻⡏⠸⣷⣤⣤⣬⣙⣿⣷⣤⣤⣴⣶⣾⡻⠋⢠⣶⣖⠒⣂⠭⣭⣟⣀⡛⠻⢿⠏⣤⡾⢋⣴⣾⢟⣑⡚⣋⣽⣷⡾⠋⠻⠅⠰⡿⠿⠛⠀⠉⢋⡏⠁⠘⠻⢿⣿⡆⠻⠟⠙⣓⠲⣜⡢⣙⠓⠊⠛⢷⣦⡙⢷⣀⠰⣾⠟⢋⣐⣛⣭⠭⢥⠶⣂⣤⡌⠙⢿⣶⣦⣤⣄⣠⣾⣿⣋⣠⣤⣥⣥⢠⣿⣿⣿⣿⣿⣿⣿⠀⣸⣿⣿⡆⠀⢸⡇⠀⣿⡇⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣾⣷⠘⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡌⢆⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⢨⣿⢸⣿⣿⣿⣿⠇⢸⡇⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣇⠀⠀⠀⠀⠀⠈⣿⣧⠀⣿⠀⠀⢸⣿⣿⡇⠀⣿⣿⣿⣿⣽⣿⢤⡕⢄⣘⠛⠿⠿⠟⠛⠻⣿⣤⣄⠭⣤⡚⢿⣌⠻⣿⣧⣝⠿⠶⢶⣶⠌⣀⣀⣴⣛⣠⣬⣯⠵⢟⣫⣾⣿⠛⣁⣤⡤⡖⠀⠀⠀⠀⠠⢤⡀⢲⡆⣢⠔⠀⠀⠀⠁⢀⣴⣤⣍⠈⠊⠻⣎⠷⢀⠈⠱⢮⣥⣤⡛⣧⣤⢤⢽⣶⣶⡶⠞⣫⣾⣿⠏⣠⡿⣂⣬⠍⣉⣭⡍⠛⠿⠿⠿⠿⠛⠁⠘⣭⣿⣿⣿⣿⣿⡿⠀⣿⣿⣿⠀⠀⢸⡇⠀⣿⡇⠀⠀⠀⠀⠀⠀⣍⡀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠁⣿⡇⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⡠
⠀⡇⠈⠆⠀⠀⠀⠀⢸⡏⠀⠀⠀⢸⣿⢸⣿⣿⣿⣿⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢩⠀⠀⠀⠀⠀⠐⢿⣿⠀⢿⡄⠀⢻⣿⣿⣿⢀⢹⣿⣿⣿⣿⣿⢹⣿⡌⣛⠛⠷⢶⣮⣭⣀⡈⠙⠻⣿⣦⣍⡓⢼⣷⣌⡛⠻⢷⣦⣵⣀⣼⣛⣋⣐⣛⣋⣉⣰⣴⣿⠸⠋⢠⠬⠿⠛⠃⠈⠂⠈⢦⣄⠀⠀⢴⠤⠤⡄⠀⠒⣠⠂⠀⠜⠙⠛⠿⣷⣄⡄⠹⣧⡘⢿⣧⣀⣉⣛⠿⠦⠝⢛⣠⣀⣠⣤⡾⠟⢛⣡⣬⣥⠖⣩⣴⣾⠛⠋⣀⣤⣤⣤⣶⠖⠛⠃⢼⣿⢻⣿⣿⣿⣿⡇⢸⣿⣿⣿⠀⠀⣸⡇⠀⣿⡇⠀⠀⠀⠀⠀⠀⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣿⣿⣯⣿⣿⡇⠀⠀⠀⢀⡇⠀⠀⠀⠀⢰⠁
⠀⠇⠀⠀⠀⠀⠀⠀⢸⠁⠀⠀⠀⢸⣿⢸⣿⣿⣿⣿⠀⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣄⡀⠀⠀⠀⠀⠀⢻⣿⠀⢸⣧⠀⠘⣿⣿⣿⡀⢸⣿⣿⣿⣿⣿⣞⣿⠀⢩⣭⣭⣭⣤⣤⡌⢭⣤⣀⢌⠻⣮⠹⣷⣮⣭⠛⠓⣀⣤⣭⣉⡛⠻⠿⠿⣿⠻⠟⠻⠀⢀⡤⠘⠈⠀⠀⠀⠀⠀⠀⠀⠀⠙⠂⠀⠐⢮⠐⠀⠆⡜⠁⠀⠀⠀⠀⠀⠀⠀⠁⠛⢧⣌⠓⠲⢬⡙⣛⠛⠿⠿⠝⣿⣟⣋⣽⣥⡀⠒⢛⣭⣽⡎⣰⡾⠋⣀⣤⠬⢉⣭⣥⣤⣤⣩⣽⠁⢼⡇⣾⣿⣿⣿⣿⠀⢸⣿⣿⣿⠀⢀⣿⠃⢠⣿⠇⠀⠀⠀⠀⠀⠀⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⢿⣿⢾⣟⢻⢿⡇⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀
⢰⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⣿⢸⣿⣿⣿⣿⠀⣿⡇⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠛⠓⠀⠰⢼⣿⡇⠸⣿⣦⣾⣿⣿⡿⠇⠂⢿⣿⣿⣿⣿⣿⣯⠀⣈⣉⣙⣻⣟⣛⠛⠳⠶⣍⠃⠀⠀⢰⡈⠍⠉⠠⢾⡟⣋⣿⣿⣿⣿⣿⣿⠟⠀⠠⣴⡆⠉⠀⠀⠀⣀⢠⠀⢰⡇⠈⠑⠀⠀⢀⡀⢀⠩⠉⠀⡀⠀⠀⠀⠉⠉⢸⡀⢀⠀⡀⠀⠀⠈⠻⣦⠀⠀⠈⢹⣿⣯⣭⣿⣿⣿⣿⣿⠻⣷⣄⠙⢋⡄⠀⠀⠀⠩⠶⠞⢛⠿⣛⣛⣛⣛⣋⠀⣸⣵⣿⣿⣿⣿⡇⡄⠿⠿⠿⣿⣤⣿⣿⠀⢸⣿⠀⠀⠠⠶⠶⠚⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠤⠀⠀⠀⣿⡇⢸⣿⣾⣟⣽⣿⡇⠀⠀⠀⠸⡇⠀⠀⠀⠀⠀⠀
⠘⠀⠀⠐⠀⠀⠀⠀⢘⠀⠀⠀⠀⢸⡟⢸⣿⣿⣿⣿⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣷⠒⠒⠒⠤⠀⠀⠘⣿⣇⠀⣉⣉⣩⣤⣶⣶⣿⢀⢸⣿⣿⣿⣿⡝⢿⣧⢈⣉⡙⠛⠿⣿⣶⣬⣒⣒⠀⠀⠀⠤⠅⣴⡇⠰⠲⠶⢦⣭⣉⣉⣉⣉⣉⣙⣒⣂⠈⠁⠀⠀⣴⡏⡇⠸⠸⠼⠇⢀⠀⡀⣀⠐⢒⣲⣬⣷⣐⠒⣀⡄⠀⠀⠀⢈⣧⢸⡀⣿⠀⣄⠀⠠⠁⠀⢐⣒⣘⣋⣋⣉⣋⣉⣩⣭⡷⠖⠂⣿⣷⡄⠶⠤⠀⠀⢒⣊⣩⣴⣾⡿⠿⠛⠛⠁⢠⣿⣿⣿⢿⣿⣿⢃⢡⣿⣷⣶⢶⣦⣤⡅⠀⣼⣿⠀⠀⠀⠀⠤⠤⠖⣶⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⢿⡇⢸⣿⢹⣿⣿⢿⡇⠀⠀⠀⠸⡇⠀⠀⠀⠀⡄⠀
⠃⠀⢀⡇⠀⠀⠀⠀⣸⠀⠀⠀⠀⢸⡇⢸⣿⣿⣿⣿⠀⣿⡇⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⣿⡏⢁⠀⠀⠀⠀⠀⠀⢿⣿⠀⢹⣿⣏⠀⢻⣿⣿⡆⢸⣿⣿⣿⣿⣿⡎⣿⡌⢿⣮⣭⣐⡢⠉⠙⠛⠿⠿⢿⣿⠿⠿⢿⣧⡌⠛⠻⢶⣶⣶⣶⣶⣦⣭⣭⣝⡋⠀⢠⠀⣾⢹⠇⡇⡇⡀⡆⠀⢸⣇⢰⡸⡀⠉⠀⠹⠃⠈⢡⣿⢃⡆⠀⠀⠘⢿⠸⡇⢻⠀⠿⡄⠈⡇⠀⠀⣀⣠⣬⣤⣶⣶⣦⣴⣶⡾⠿⠛⠋⠙⠻⠿⠿⡿⣿⠿⠿⠛⠋⠁⢄⣀⣤⣤⠄⣸⣿⣿⢏⣿⣿⡿⠀⣼⣿⣿⠏⠀⣽⣿⠃⢀⣿⡇⠀⠀⠀⠀⠀⠀⠀⣸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⢻⡇⠀⣿⢸⣿⣿⣼⡇⠀⠀⠀⢸⡇⠀⠀⠀⠀⣤⠀
⠀⠀⠸⠀⠀⠀⠀⠀⣿⠆⠀⠀⠀⢸⡇⢸⣻⣿⣿⡇⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⢠⠀⠀⢸⣿⡄⠈⣿⣧⠀⠘⣿⣿⣷⠀⢿⣿⣿⣿⣿⣧⢻⣏⠀⣆⣉⣙⣛⣛⣛⣛⣛⠀⢸⣿⡇⡄⠛⠻⠿⠷⠦⣤⣀⣉⣉⡛⠿⠿⢟⣛⣀⢠⣸⡄⡏⣸⠀⣇⣧⠁⢀⡄⢰⣿⣆⢧⡹⡄⠀⠀⠀⢀⡾⣣⣿⣴⠇⠀⢸⣌⠃⣇⢸⠀⡆⠀⡀⡇⢠⠀⣟⡛⠿⠿⠿⠿⠿⣛⣁⣬⠴⠾⠿⠟⣛⡀⣾⣿⠀⢰⣶⣿⣿⣿⢟⡋⠩⠀⢰⣿⢏⣵⣿⣿⣿⡇⢂⣿⣿⣿⠀⢰⣿⡟⠀⢸⣿⡇⠀⢀⠀⠀⠀⠀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⣿⢸⡟⣿⣿⡇⠀⠀⠀⢸⡇⠀⠀⠀⠀⠘⡆
⠂⠰⢁⢐⠀⠀⠀⠀⡿⠀⠀⠀⠀⢸⡇⢸⣿⢹⣿⡇⡄⣿⡇⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⣿⡇⠜⠀⠀⠀⠈⠀⠀⠸⣿⣷⠀⢸⣿⣦⢠⠹⣿⣿⡊⢸⣿⣿⣿⣿⣿⡜⣿⡆⢙⣛⣛⣙⡛⠛⢛⣛⠀⢸⣿⠇⠶⠶⠶⠿⠟⠛⣋⣩⡉⠭⠛⠛⠻⠟⠛⠁⣾⣿⡟⣷⡿⣰⣧⠏⠠⠿⣃⡄⠩⡻⣦⡱⡹⡀⠀⡰⣫⣾⣿⣿⣣⠆⠰⣮⡙⠷⠈⢸⡀⣷⡆⠁⢿⠈⠀⣻⠛⠻⠿⢿⣟⠛⢋⣭⣑⡻⠿⠶⠶⠤⠥⢻⡿⠀⢸⠿⠟⠛⠛⢛⣛⡛⠂⣼⢏⣾⣿⣿⣿⣿⠀⣼⣿⣿⠇⢒⣿⣿⠃⢀⣿⡿⠁⢀⠟⠀⠀⠀⠀⠀⣸⡇⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⣼⡇⠀⣿⣼⣿⣿⢸⡇⠀⠀⠀⢸⡇⠀⠀⠀⠀⡄⣱
⠀⠇⢀⠎⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⣼⣿⢸⣿⡇⡇⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⡇⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⡆⠀⢿⣽⣟⡄⢻⣿⣧⠈⣿⣿⣿⣿⣿⣷⡸⣿⡆⢭⣙⣛⠻⠿⠶⠌⠀⢸⣿⣠⣴⣶⣾⣿⣿⡿⣿⣿⠿⠿⡿⠿⠿⠿⠿⠇⣹⣿⠀⡟⢃⡟⣼⢸⣷⡈⠋⣄⣀⠙⢜⢿⣷⡁⠈⠠⠵⢾⣿⠟⠁⣸⣗⠈⠙⢂⡆⠈⣧⢹⡇⠂⢸⣇⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣈⡇⠀⢩⣥⠶⠾⠿⢛⡋⠁⣼⡟⣼⣿⣿⣿⣿⡇⢀⣿⣿⡏⢠⣾⣿⡏⠀⣸⣿⣷⣖⣾⡄⠀⠀⠀⠀⠀⡏⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⣿⣿⣿⣿⢸⡇⠀⠀⠀⢸⡇⠀⠀⠀⠀⢇⠁
⠸⢀⠂⠇⠀⠀⠀⠀⣿⠁⠀⠀⠀⢸⡇⣿⣿⢸⣿⡇⡇⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣟⠁⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡄⠈⣿⣿⣿⣼⠿⠟⠂⠹⣿⣿⣿⣿⣿⣧⢻⣷⡈⣿⣋⣀⣠⣤⣴⠶⠻⠟⢛⣻⣭⣭⡍⠁⣤⣶⡆⠒⠶⢶⣶⣶⣶⠗⠀⣿⣿⠀⠁⣼⢱⡇⠘⠛⢿⣦⡛⠿⠀⠀⠁⠉⠩⠷⡄⠁⠀⠀⠀⢰⣿⡿⢃⣴⠿⠃⠠⢹⡆⢻⡆⢸⣿⠄⢻⡷⣶⣶⣶⣶⡦⢴⣾⣧⡌⠉⣭⣙⣛⡛⠿⠿⣦⣦⣤⡀⠀⣙⣻⠃⣰⡿⣰⣿⣿⣿⣿⡿⠃⡘⠻⠿⣤⣿⣿⡿⠀⢰⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠁⢰⠈⢀⢼⡇⠀⣿⣿⣿⣿⢸⡇⠀⠀⠀⢺⡇⠀⠀⠀⠀⠘⢂
⣇⠢⠀⡴⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⣿⣿⢰⣿⡇⣧⣿⡇⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⣿⣷⡀⠙⠛⣉⣤⡶⣿⣿⣆⠙⣿⣿⣿⣿⣿⣇⢻⣷⠸⡿⠟⢛⣩⡅⢠⣾⣿⡦⣯⠅⠄⢀⣼⣿⠋⠘⠛⢻⣶⣶⣤⣤⣶⠀⢸⣿⠀⢰⡇⢋⣾⠛⠓⢀⡙⠛⠀⠀⠀⠀⣠⢤⡀⠀⢠⠀⠀⠀⢀⡙⠂⠛⠁⠐⠻⣷⠘⢿⣾⡇⡈⣿⣇⢲⣤⣥⣭⣵⣶⠞⠛⠈⢿⣿⣆⠉⠉⣭⣥⣾⣷⡄⢨⣝⡛⠿⣿⠏⣸⡿⣰⣿⣿⣿⣿⡿⢁⣾⣿⣿⣶⣤⣍⡙⠁⢠⣿⣿⣿⣶⣏⠀⠀⠀⠀⠀⠀⠒⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠂⠀⠀⢹⡇⡇⣿⣿⣿⣿⢸⡇⠀⠀⠀⣨⡇⠀⠀⠀⠀⡀⠈
⡏⡄⢰⠁⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⣿⣿⣸⡯⠃⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣛⠛⠂⠀⢀⡀⠀⠀⠀⢠⣆⢸⣿⣿⣷⠀⢻⣿⣿⠀⠹⣿⣿⣆⠈⢿⣿⣿⣿⣿⣧⠻⣧⠀⣾⡿⠁⠀⣼⣿⡿⠙⠁⠀⢰⣿⡿⠡⠾⠟⠛⠫⠭⠭⠉⠁⡀⠀⣸⣟⢰⡏⢀⣭⣤⣴⣶⠟⠁⠀⡖⠀⠀⠀⢫⡀⠀⠀⡈⠀⠀⠀⠸⣷⠀⠀⣽⠳⢶⣦⣤⣀⠹⡇⠁⢸⣿⠀⡉⠉⠭⠭⣝⣛⠻⠷⣦⣻⣿⣧⠀⠈⢿⣿⣿⣿⡀⢻⣿⣷⡄⣰⡿⣡⣿⣿⣿⣿⠟⢀⣾⣿⣿⢿⣿⣿⣿⠃⢀⣾⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⡇⣿⣿⣿⣿⢸⡇⠀⠀⠀⣿⣧⠀⠀⠀⠀⢱⠀
⠁⢡⠇⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⢸⡇⣿⣿⢸⣷⢠⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⢠⠀⠀⠀⢀⠚⣿⣿⣿⣇⠀⢻⣿⣧⣆⢻⣿⣿⣦⠈⢻⣿⣿⣿⣿⣧⣻⣧⢘⠁⢀⣼⣿⠟⠀⣀⠀⣰⣿⡟⢀⣨⣴⣶⡶⠿⣣⣶⣶⣶⠇⣼⣿⠁⣤⡅⣼⣿⠿⢛⣵⠎⠀⠈⠙⢿⣶⣦⡄⢙⣈⠉⢡⣴⣾⠗⠁⠁⠀⠘⣌⢶⣌⠛⢿⣿⡇⣴⠄⣿⡇⠅⣷⣶⣤⣴⡖⢶⣦⣬⣍⡂⠹⣿⣆⠀⣄⠑⢻⣿⣧⠀⠹⡿⣰⡟⣰⣿⣿⣿⡿⠋⢠⣾⣿⣿⣿⣿⣿⣿⠃⢀⣾⢣⣿⣿⣿⠋⠁⠀⣀⠐⠒⠒⠒⠛⠚⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⢸⡇⡇⣿⣿⣿⣿⢸⡇⠀⠀⠀⢿⣿⠀⠀⠀⠀⠀⢇
⠀⡎⠐⠁⠀⠀⠀⠀⣿⠆⠀⠀⠀⣼⡇⣿⣿⢸⢿⢸⡟⣿⡁⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⠉⠉⠙⠋⠈⠛⠀⠀⣈⡛⠨⣿⣿⣿⣆⠀⢿⣿⣿⣇⠹⣿⣿⣧⡁⠹⣿⣿⣿⣿⣷⡹⣦⡀⢾⣿⠟⢀⣾⠋⠀⣿⣿⠀⠿⠛⠋⢀⣴⣿⡿⠟⠉⣤⠀⣿⡿⢸⣿⣿⡈⢠⣾⣿⠁⠀⠈⠀⠀⠀⠉⣿⡁⢿⣿⣦⡹⣯⠁⠀⠀⠀⠀⠀⠸⡄⠹⣷⣶⡜⢱⣿⠀⣿⣇⠀⣷⡌⠛⢿⣿⣷⣌⠉⢛⣿⡇⣿⣿⠀⠹⣷⡀⢻⣿⡆⢀⣶⢏⣼⣿⣿⣿⡿⠁⣠⣿⣿⣿⢿⣿⣿⣿⠃⠀⣾⢟⣿⠿⡟⠻⠟⠃⢸⡿⠘⠖⠒⠒⠂⣤⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⢸⡇⡇⢹⣿⣿⣿⢾⡇⠀⠀⠀⢸⣿⠀⠀⠀⠀⠢⠘
⢰⠏⠀⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇⣿⣿⣼⣷⢰⡧⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢙⣿⠅⠀⢠⡀⠀⠀⠀⣌⣿⣿⣿⣿⣿⣯⢻⣆⠈⢿⣿⣿⣇⠹⣿⣿⠷⠐⠙⣿⣿⣿⣿⣿⣎⢿⣎⠋⣠⡾⠃⣠⠀⣿⣿⡇⠁⠀⣠⣿⡿⠯⠀⢠⡾⠃⠀⠿⠁⣾⠈⣿⣷⠈⢻⢏⡌⠈⠁⠀⠀⠀⢰⣿⢃⠘⢿⣿⣟⡒⣄⠀⠀⠀⠀⠀⠀⢿⡌⢿⠇⢠⣿⠏⠀⠈⠿⢀⠈⢿⣆⠑⢾⣿⣿⣦⠀⢻⣷⣿⣿⠀⣄⠘⢷⣄⠻⣡⡾⣱⣿⣿⣿⣿⠟⠁⠰⢿⣿⣿⣣⣾⣿⣿⠃⢀⣾⢏⣾⠛⢠⣿⣿⢷⡀⠀⠀⠀⢀⠀⠀⠐⣿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⡇⢸⣿⣻⣿⢸⡇⠀⠀⠀⣿⣿⠀⠀⠀⠀⢃⠐
⠸⠰⠀⠇⠀⠀⠀⠀⣿⠀⠀⠀⠀⣿⡘⣿⣿⡪⢹⢸⡇⣿⠧⠀⠀⣀⠀⠀⢀⠀⠀⠀⠀⠀⢸⣻⣿⡀⠀⢸⡆⠀⠀⠀⡘⠋⡉⠉⠻⢿⣿⣿⣿⣦⠀⢻⣿⣿⡿⢛⣥⣾⣿⣌⠌⢿⣿⣿⣿⣿⣧⡹⣦⡉⠀⣼⡿⠀⢹⣿⡇⠀⢰⣿⣿⠁⠀⢴⠟⣡⣶⡇⠆⠀⣼⡇⠸⣿⣷⡀⢺⡇⠈⠁⠀⠀⢰⠛⠁⠸⣇⢼⢻⡏⠁⠘⣧⠀⠀⠀⠈⠀⢸⣷⠄⣠⣿⠏⠠⣷⡀⢀⠀⣷⣄⠻⢧⡈⢿⣿⣿⡆⠘⣿⣿⡏⠀⢿⣧⠈⠋⣠⢏⣴⣿⣿⣿⣿⠏⢀⣼⣿⣦⣍⠻⢿⣿⣿⠃⠀⣼⢋⣾⣿⡤⢺⣿⣶⢾⠁⠀⠀⠀⠘⠀⠀⠀⡿⢠⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠠⣸⡇⡇⢸⣿⢽⣿⢸⡇⠀⠀⠀⢹⣿⠀⠀⠀⠀⠘⢀
⡇⣢⠂⠀⠀⠀⠀⠀⡟⠀⠀⠀⢀⣿⢰⣿⣟⣿⠀⣿⡇⣿⡆⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠸⣿⣿⠏⠀⠈⠀⠈⠀⠀⠉⠉⣁⣀⣠⣼⣿⣿⣿⣿⣧⠀⠛⣡⣴⣿⡟⢿⣿⣿⣧⡠⠻⣿⣿⣿⣿⣿⣌⡻⣦⡙⢁⠀⢸⣿⡇⠀⣾⣿⠃⠀⣀⣴⡾⠟⠋⣠⡦⢸⣿⠁⢀⡌⢻⣿⡌⠀⠀⠀⠀⠀⠏⠀⠀⠀⢻⠨⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⠸⢃⣼⣿⢃⡀⢠⢻⣷⢰⣄⡘⡟⢿⣦⣐⠈⢛⣿⣇⠀⢿⣿⣧⠀⣸⠟⣠⡞⣡⣿⣿⣿⣿⡿⠃⢠⣿⣿⣿⣟⣿⣿⣦⡌⠃⢀⣾⢡⣿⣿⡟⠀⣰⣿⣿⣿⡟⠀⠀⠀⠀⠘⠁⢶⣿⣖⠀⠀⠀⠀⠀⠘⠇⠀⠐⠊⠁⠀⢹⣷⣧⢸⣿⢸⣿⢸⡇⠀⠀⠀⢘⣿⠀⠀⠀⠀⠀⢄
⣧⠃⡸⠀⠀⠀⠀⠀⡇⠀⠀⠀⢸⣿⢸⣿⣷⡿⠀⣿⣿⣿⠁⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⡶⣤⡉⠁⠀⠀⠀⠀⠠⢀⣐⣀⣛⣿⡻⠁⢿⣿⣿⣿⣟⣷⡀⠙⢿⣿⣿⣆⠻⣿⣿⣷⡄⠹⣿⣿⣿⣿⣿⣷⣎⣿⣆⠀⣾⡟⠀⣰⣿⠇⢠⣾⡿⠋⢀⣴⡿⣫⣤⣿⡟⢠⣾⠃⠀⢻⠏⠀⠀⠀⠀⠀⠀⠀⣀⣤⠀⢸⡄⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⢾⣿⠇⠘⣿⣄⠸⣿⢣⣙⢷⣦⡒⢝⢿⣷⡄⢻⣿⡆⠈⣿⣿⠀⢠⡾⣩⣾⣿⣿⣿⣿⠟⠀⣴⣿⣿⣿⣿⣿⣿⣿⠟⠁⣠⡿⣱⣿⣿⣯⡀⢰⣿⣿⣟⣹⣿⣷⠀⠀⠀⣀⠀⠀⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠔⠀⠀⠀⢸⣿⣿⡄⣿⣾⣿⢸⡧⠀⠀⠀⢸⣿⠀⠀⠀⠀⢸⡈
⠊⢰⢫⠀⠀⠀⠀⠀⡇⠀⠀⠀⢸⣿⢸⣿⡿⡇⢰⣿⣿⣿⠀⠀⡀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠃⣿⡇⠀⠀⡄⠀⠀⠀⠀⠈⠉⠁⠰⣥⣦⢿⣿⣿⣿⣿⣿⣿⣄⠀⠻⣿⣿⣿⣌⢻⣿⣿⣦⠘⢿⣿⣿⣿⣿⣿⣿⣿⣷⣌⡁⢴⣿⠋⣰⣿⠟⣠⣴⢟⣫⣾⡟⠁⣿⠁⠿⢁⣴⣷⠘⠀⠀⠀⠀⠀⠀⣠⠞⠁⡁⣤⢈⣭⠄⢈⠙⢦⡀⠀⠀⠀⠀⠀⠈⢏⣶⣦⡌⠻⡄⣿⠇⢿⡧⣝⠿⣦⡑⠻⣿⣆⠻⣿⡆⠈⣩⣾⣯⣾⣿⣿⣿⣿⣿⠟⢠⣾⣿⣿⣿⣿⣿⣿⡿⠋⢀⣶⣏⣼⣿⣿⣿⡿⠁⠺⡿⠛⠿⠛⠛⣯⣠⠀⠸⣿⡧⠰⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢸⣏⣿⡇⢹⣿⣿⢸⣿⠀⠀⠀⣼⣿⠀⠀⠀⠀⢀⢧
⢌⠆⠌⠀⠀⠀⠀⠀⣇⠀⠀⠀⢸⣿⢸⣿⡿⡇⢸⣿⣿⣿⠂⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠶⠰⠇⠀⠀⠀⠀⠀⠀⠀⠴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡝⣧⡀⠙⢿⣿⣿⣷⣙⣿⡿⠗⣨⡉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣦⣇⠸⡿⢃⣼⠟⣡⡾⠋⣿⠏⠀⢿⣠⣶⢸⣿⠑⠀⠀⠀⠀⢀⠀⠰⠃⠰⢿⡉⣿⡀⣿⡀⢸⠀⠈⢷⢠⡀⠀⠀⠀⠀⠈⢿⣿⣿⣦⡜⢿⠀⢹⣷⠘⣷⣌⢻⣦⠹⣿⡆⣩⣵⢾⣿⣿⣿⣿⣿⣿⡿⠛⢁⡐⢿⣿⣿⣿⣿⣿⣿⠟⠀⢠⡾⣫⣿⣿⣿⣿⣿⣶⣶⣶⣶⣤⣀⡀⠀⠿⠃⠀⠐⣿⡧⣿⣿⣤⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠆⠀⢸⣯⣿⡇⢸⣿⣯⢸⣿⠀⠀⠀⣿⣿⠀⠀⠀⠀⠘⡘
⣎⠊⡰⠁⠀⠀⠀⢰⣿⠀⠀⠀⢸⣿⢸⣿⣇⠃⢸⣿⣿⣿⠄⠀⠀⠀⠀⠘⠛⠁⠀⠀⠀⠀⠚⠛⠛⠓⠒⠖⠒⠲⠲⠲⠶⠶⢦⣴⣤⣬⣭⣿⣿⣿⣿⣿⣿⣿⣎⠻⣆⠀⠙⢿⣿⣿⠟⣡⣾⣿⣿⣦⣔⢍⡻⣿⣿⣿⣿⣿⣿⣿⡷⣦⣘⠁⣾⣟⠀⣸⡿⠀⠀⣾⡿⠁⣾⡇⠀⠶⠿⢋⠀⢀⡴⢣⠆⣾⣿⠀⣿⡃⢻⡇⢸⠀⣤⠈⠀⢉⠂⠻⠶⠤⠀⠀⢿⣿⠘⣿⣿⠀⠋⣿⡆⢈⣻⣷⡙⢃⣠⢔⣿⣿⣿⣿⣿⣿⡿⠛⢁⣠⣾⣿⣿⣦⡙⢿⣿⣿⠟⠁⢀⡴⢋⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⡆⠀⠀⢠⣤⣯⣤⣽⣽⣿⡄⠀⠀⠀⠀⠀⣤⠄⠀⠀⠀⠀⢸⣿⣿⣷⢸⣿⣿⢸⣿⠀⠀⠀⣿⣿⠀⠀⠀⠀⢀⠑
⢂⠔⢁⠂⠀⠀⠀⢠⣿⠀⠀⠀⢸⣿⢸⣿⡿⠆⣿⣿⢸⣿⡀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣶⣶⣶⣶⠖⠛⠀⢀⡀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡙⣷⣄⠀⠛⣡⣾⣿⣿⡹⢿⣿⣿⣷⣍⡲⢝⠿⣿⣿⣿⣿⣿⣶⣭⡻⣦⣉⠰⠿⠃⢀⣼⡿⢡⢸⣿⢣⣤⠂⠀⡟⢀⣾⢃⡏⣼⣿⣧⢀⣿⣿⣼⣧⡈⣇⢻⣷⡀⠸⡇⡄⠀⠀⢠⣤⡀⣿⠐⡜⣿⣦⠀⠸⣿⠀⣋⣥⢾⣯⣷⣿⣿⣿⣿⡿⠛⠁⣠⣴⣿⣿⣿⠟⣵⣿⣿⣦⡝⠋⠄⣴⠟⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠉⠛⠂⠀⢠⣤⣤⣤⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⣿⣿⢸⣿⠀⠀⠀⢿⣿⠀⠀⠀⠀⠈⢢
⣪⠂⠀⡀⠀⠀⠀⢸⣿⠀⠀⠀⢸⣿⢸⣿⡇⠀⣿⣿⣼⣿⠀⠂⠀⠐⣆⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡏⢨⠆⠀⠀⠠⣄⣚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⢿⣷⡄⠈⠻⢿⣿⣿⣦⣽⠿⣿⣿⣿⣷⣅⠪⢝⠿⣿⣿⣿⣿⣿⣷⣿⣿⡶⣠⡘⠛⠱⣇⢸⣿⡾⠁⠂⣸⠁⣼⠏⡾⢠⡯⢸⣿⠸⣿⣿⣿⣿⣷⢹⡌⣿⣷⡀⠀⣿⣠⠀⠀⢿⣧⣿⡀⢿⡜⠟⢡⡀⠰⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⣊⣴⣾⣿⣿⠟⣽⣯⣾⣿⣿⠟⢁⠄⣠⡾⢋⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠦⠞⡃⠰⣼⣽⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⢀⠐⠀⠀⢸⣿⣿⣿⠀⣿⣿⢸⣿⠀⠀⠀⣿⣿⠀⠀⠀⠀⠘⠢
⠤⠴⠚⠀⠀⠀⠀⢸⣿⠀⠀⠀⢸⣿⢸⣿⣇⠀⣿⣿⢹⣿⠀⠀⠾⠀⠀⠀⢀⠀⠀⠀⠀⠀⣿⣿⣿⠁⢸⣇⠀⠀⠀⠠⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣷⣄⠀⠙⣿⣿⣿⣿⣮⡻⣿⣿⠋⣰⣦⣝⠪⣙⠿⣿⣿⣿⣿⣿⡇⢿⠇⣿⢷⣶⣌⡉⢁⡶⢳⣿⠰⠫⢾⡇⣾⢃⢸⡟⢁⣤⣙⠿⣿⣿⣼⣷⠘⢻⣷⡄⠛⣿⠈⢀⠀⠛⣋⣡⠄⠂⠑⠙⠃⠼⠿⢿⣿⣿⡿⠟⠉⢀⣴⣦⡈⠻⣿⣿⢏⣴⣿⣿⣿⠟⢁⠄⣡⡾⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣅⣈⠁⠀⢹⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠋⠀⣄⠀⢸⣿⣿⣿⠀⣿⣿⢸⣿⠀⠀⠀⣿⣿⠀⠀⠀⠀⢠⡉
⠶⢅⠒⠀⠀⠀⠀⢸⡇⠀⠀⠀⢸⣿⢸⣿⡇⠀⣿⣿⢹⣿⣴⣶⣦⣄⠉⠀⢀⠀⠀⠀⠀⠐⢼⣿⣯⣀⣼⠇⠀⠀⠀⢀⣐⡶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡻⣷⣤⡀⠙⠿⣿⣿⣿⡾⢁⡾⣿⣿⣿⣿⣶⣕⡪⠛⢿⢩⣶⣶⣾⣶⡶⠦⠙⠛⠁⡄⣥⠘⢿⠄⢰⣷⣄⢿⠋⡘⠛⠘⣿⣿⣷⣶⣶⣌⢻⣷⡌⢙⡛⠇⠼⠀⢘⢨⢸⣿⣷⠀⢻⣿⣿⣿⣿⣿⠈⠟⠉⣀⣴⣾⣿⣿⣿⣿⣄⠛⢿⣿⣿⠿⠋⠀⣀⣴⡾⣻⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⡛⣍⠁⠀⠀⠀⢹⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠃⠀⠄⠀⠉⣀⣸⣿⣿⣿⠀⣿⣿⣼⣿⠀⠀⠀⣿⣿⠀⠀⠀⠀⢈⣉
⠜⢄⠉⠀⠀⠀⠀⢸⡇⠀⠀⠀⢽⣿⣼⣿⡇⢠⣿⣿⢸⣿⠁⠀⠁⠀⠉⠁⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⢠⣾⣿⣿⢂⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⣿⣿⣦⣀⠨⢙⠛⢠⣾⣿⣷⣝⡻⣿⣿⣿⣿⣦⣀⢸⣿⣿⣿⣿⣿⣷⠀⠀⠀⠣⣿⢸⢀⡄⣺⣿⣿⣤⣼⣿⣿⣰⣿⣿⣿⣿⣿⣿⢶⣌⡁⣿⣿⣦⠀⠀⢸⠸⠀⣿⣿⡄⢸⣿⣿⣿⣿⣿⠁⣴⣿⣿⣿⡟⣻⣿⣿⣿⡇⣿⠸⠟⠁⣄⣤⣾⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣈⡿⢿⠍⣩⣶⣦⠀⠀⠘⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠘⠀⠠⠀⠚⠛⠙⢹⣿⣿⣿⠀⢸⣿⣿⣿⠀⠀⠀⣿⣿⠀⠀⠀⠀⢀⡤
⠌⠄⢉⠀⠀⠀⠀⢸⣿⠀⠀⠀⣾⣿⣿⣿⣇⢸⣿⣿⢸⣿⠀⠀⠘⠆⠀⠀⠀⠀⠀⠀⠀⢰⣸⣿⣿⣿⡏⠀⠀⠀⢥⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢿⠀⡬⡛⠿⣿⡿⡛⢶⣶⣝⡻⣿⣿⢾⣿⣿⣿⣿⣿⣿⠀⠀⠈⢻⡀⡎⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣼⣿⣿⢻⣻⣿⡇⡀⠀⡦⠼⠉⠁⠀⣸⣿⣿⣿⣿⣿⢰⣿⣿⣿⣛⣿⣿⡿⢟⣛⣃⣉⣀⣉⡚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⣶⡆⢸⡟⠉⠃⠀⠀⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠄⠀⢸⣿⣿⣿⠆⢸⣿⡇⣿⠀⠀⢤⣿⣿⠄⠀⠀⠀⢠⡴
⡌⢌⢦⠁⠀⠀⠀⢸⣿⠀⠀⠀⣿⣿⣿⣿⣿⢸⣿⣿⢼⣿⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠙⠛⠛⠋⠀⠀⠃⠀⡀⣲⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢡⣶⣶⣶⣶⣶⣦⠁⠈⢱⣿⢸⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⢰⣷⣆⠊⠛⠃⠘⠫⣿⣿⠿⢿⣿⣿⣿⣟⠿⣿⣿⣿⣿⣿⣿⣿⣿⢉⣽⡿⠃⠃⠀⠱⣶⣾⣿⠀⣿⣿⣿⣿⣿⣿⢸⣿⢃⣄⢿⣿⠿⠃⣾⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣷⣘⣇⣼⣇⢫⡁⠰⣾⣿⠈⠻⢿⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠄⢸⣿⡇⣿⠀⣠⣸⣿⣿⡇⠀⠀⠀⡠⢢
⠰⣸⡦⠀⠀⠀⠀⢸⡿⠀⠀⠀⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠋⠀⠀⠈⠁⣰⣿⠉⠀⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⠟⢠⣤⣴⣶⣾⣭⡍⠻⣿⢡⡈⣿⣿⣿⣿⣿⣿⠘⣿⣿⡇⠀⠀⠀⠀⢿⣿⠂⡌⣩⡍⡿⢿⣿⣿⢿⣿⣿⡟⣭⠹⠏⣈⡈⠀⠀⠀⠀⢀⣿⣿⣿⠀⣿⣿⣿⣿⣿⡿⠀⢿⠘⠟⠈⠴⢿⡇⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠀⠁⠰⡦⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⣸⣿⡇⣿⠀⣿⣿⣿⣿⡇⠀⡀⠈⣰⣳
⡇⢩⡇⠀⠀⠀⠀⢸⣷⠀⠀⠀⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⡇⣿⡇⠀⠀⠀⠀⠀⠀⣸⡄⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⡀⣿⣿⣿⣿⣿⡟⠁⠀⠁⠻⠇⠿⣿⣿⣿⣿⣿⢐⣿⣿⣿⣦⡄⡀⠀⠀⠁⠄⡇⢸⡇⣷⣷⠙⣿⣿⣿⠏⢀⣿⢰⡇⣸⡷⠂⠀⣠⣴⣿⣾⣿⣿⡄⢰⣶⢻⣿⡿⠁⣼⣿⣿⣿⣿⣿⡆⣿⢸⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠠⣼⡆⠀⠀⠀⢿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⢸⣿⣿⣿⠄⣿⣿⡇⣿⠀⣿⣿⣿⣿⡇⠀⠁⠄⡙⣿
⠇⡸⠃⠀⠀⠀⠀⢸⣿⠀⠀⠀⣿⣿⣿⣿⣿⣄⣿⣿⣿⣿⠀⠀⠰⣿⡴⠆⠀⠀⠀⠀⠀⠃⡿⠁⠀⠀⠀⠀⠀⠱⣿⡟⣠⣿⣿⣿⣿⣿⣿⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡼⠻⣿⣿⣿⡿⡇⢻⣿⣿⣿⣿⡇⢰⣶⣶⣿⣶⢶⣾⢻⣿⣿⣿⠘⠛⠛⣿⡿⡕⡁⠀⢨⡀⡆⢿⣾⣇⢸⣿⣧⠘⣿⠟⡄⢸⡿⣸⢣⣙⠁⢇⠀⢿⡇⣿⡿⠟⠛⣁⣈⣉⣼⡿⠁⠀⣿⣿⣿⣿⣿⡟⡇⣿⡀⢻⣿⣿⣿⣿⢃⠈⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢉⣿⣿⣿⣿⣿⣽⣷⣿⣗⠀⠀⠀⠘⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠸⣇⠀⠀⢸⣿⣿⣿⡃⣿⣿⡇⣿⠀⣿⣿⣿⣿⡇⠀⢀⠀⡇⣿
⢰⠁⢀⠀⠀⠀⠀⢺⡿⠀⠀⠀⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⠈⠁⣸⠿⠀⠀⡀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀⣀⢸⣧⢾⣿⣿⣿⣿⣿⣿⣿⣿⠉⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣿⣿⣿⣿⣿⡇⢠⣿⢻⣿⡿⠐⠁⢘⡹⣿⣿⡏⠁⢸⣿⣿⡏⣿⣿⣿⢸⣿⣿⣿⢠⣦⡀⡰⣾⡎⡷⠀⠀⢐⠁⢸⡈⣿⡈⠿⠿⠿⠡⢾⠇⣾⡇⡿⠈⠃⢸⣶⡀⠘⣿⣿⢂⡀⣩⣭⣙⣿⣿⣿⡆⠀⢽⣿⣿⣿⣟⣤⠀⣿⣑⠺⠿⣿⣿⣏⢿⠇⣼⣿⣿⣤⣯⣿⡿⠋⢉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣿⣿⣿⣯⣵⣿⣿⣿⡟⠀⠀⠀⠀⠹⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⡋⠀⢠⢸⣿⣿⣿⡇⣿⣾⡇⣿⠀⣿⣿⣿⣿⡇⠀⠘⠀⢇⠸
⣿⠀⢸⠀⠀⠀⠀⣿⡇⠀⠀⠀⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⠀⡰⠋⢰⡄⠀⠀⠀⠀⠀⠀⣦⠀⠀⠀⠀⠀⠀⠀⡀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢶⣟⣿⣿⠋⣥⣤⣥⣮⣝⠃⠀⠀⠸⠇⣿⣿⢇⠄⢸⣿⣿⡇⣿⣿⣿⢸⣿⣿⣿⠈⣿⡿⡇⠙⠇⣚⣇⠀⠈⠀⣴⣁⣿⣧⠀⠀⠀⠀⠀⢰⣿⡇⣯⡈⠁⢸⢻⡁⠀⠟⣿⢸⡇⣿⣿⣿⡿⣿⣿⡇⠀⢸⣿⣿⣿⣏⠛⠀⠺⢿⣿⣿⢸⣿⣿⣶⣶⣶⣬⠙⣿⡟⣁⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠈⣿⣿⣼⣿⣿⠿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠁⣦⠀⢸⣿⣿⣿⣧⣿⣿⡇⣿⠀⣿⣿⣿⣿⡇⠀⠂⡠⢺⠀
⣟⡄⢠⠀⠀⠀⠀⣿⣅⠀⠀⠀⣿⡿⣿⣿⣷⣾⣿⣿⣿⡏⢰⡧⠀⠸⠀⠀⠀⠀⠀⠀⠠⠿⡦⠤⠤⠀⠀⠀⢈⣵⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡙⠉⣤⣹⣿⣿⣿⡏⠑⢀⡉⠉⢹⠀⣿⣿⣿⣿⡇⠀⢰⣶⡿⢿⡿⢿⡜⠀⠘⣿⣿⡇⣿⣿⣿⢸⣿⣿⣿⠀⣿⣼⠇⠈⠈⣿⣷⢆⠈⠀⡸⣶⣭⡁⣶⣿⣿⣷⣶⠀⣭⣵⠯⠄⠀⢿⣿⡆⣀⡐⣽⢸⠇⢻⣿⣿⡇⣿⣿⡇⠀⣼⣿⣿⢙⣿⣿⣿⣷⠘⣿⣿⢸⣿⣿⣿⣿⣿⣿⠀⣿⡛⠚⢿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠸⠄⠻⣿⣿⣿⣿⠀⠾⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇⠈⠄⢸⣿⣿⣿⡟⢻⣿⡇⣿⡀⣿⣿⣿⣿⣧⠀⠈⢀⣼⡇
⠘⡅⠘⠀⠀⠀⠀⣿⡇⠀⠀⠀⣿⡇⣿⣿⣿⣿⣿⣿⢻⡇⠈⠀⠘⠀⠀⠇⠀⠀⠀⠀⠀⣤⣤⠀⠤⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣶⣬⣿⣷⣿⣏⠀⣴⣿⠇⠀⠈⡄⣿⣿⣿⠟⠁⠀⢸⣿⣿⡿⣼⣿⡇⠀⠀⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⠰⠿⣿⢒⠖⡀⢸⣯⢿⡆⣰⣾⣾⣿⠂⣿⣿⣿⣿⣿⣧⢸⣿⣿⣤⡘⢻⡿⠀⠸⢇⠛⣼⠀⢸⣿⣿⡇⣿⣿⡇⠀⢻⣿⣿⢸⣿⣿⣿⡿⠀⣿⣿⢘⡏⣿⣿⣿⣿⣟⠀⠛⠆⣿⣦⡀⠉⠉⠛⠛⠛⠋⢡⡉⢹⡧⢠⡄⡀⣾⣿⡟⡻⠿⠇⠈⠒⠃⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⡄⠀⠃⡀⢿⠿⣿⢹⣿⣿⣿⣿⠃⣿⡅⣿⣿⣿⣿⣧⠀⡠⣾⢹⡇
⡶⠘⡇⡀⠀⠀⠀⣿⡇⠀⠀⠀⣿⡇⣿⣿⣿⣿⣿⣿⢸⡇⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⢰⢺⣿⣧⠀⠀⠀⠀⠀⠏⣠⠈⢹⣿⣿⣿⡛⣿⣿⣿⣿⣯⠻⣎⠛⠀⠛⠻⢦⡍⠸⠋⣱⡇⢀⣾⠃⣿⠿⣟⣦⠃⢠⢸⣿⡿⢡⡹⡏⠁⠀⠀⣿⣯⡹⣿⣿⠿⢙⣉⡍⠁⠀⠀⡷⢂⢠⢠⢧⢻⣼⢁⣏⡙⡖⡟⢸⣿⣿⣿⣿⣿⣿⠸⠏⠘⡏⡀⠈⡱⢰⠃⠈⠀⠸⠃⠸⣿⣽⣧⣿⣿⠃⠀⣬⣭⣍⡸⣿⣿⣿⡇⠀⣿⣿⠀⣽⠻⣿⡟⣴⣹⣦⠀⡄⢸⡙⢷⡐⠆⢀⠀⠀⠀⠘⠀⡞⠀⡽⢻⠃⢈⠻⠄⠠⠀⠀⠀⠀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠃⠀⠀⣿⢸⣿⣿⣿⣿⡇⣿⡇⣿⣿⣿⣿⣿⠀⠡⣿⡾⣿
⢠⠰⠱⡀⠃⠀⡀⣿⠁⠀⠀⠀⣿⠁⣿⣿⣿⣿⣿⠟⣸⡇⠀⠀⠀⠀⠀⠋⠀⠀⠀⣠⠈⣿⣿⣿⡇⠀⠀⠀⠘⠂⠿⠃⠊⠾⣿⣿⣿⣍⡛⢿⠛⢛⣿⣿⣦⠀⠐⠀⠀⢠⠀⠀⣿⡇⢻⢻⢘⣿⣿⣿⠏⣰⣶⣬⣋⣥⣿⣇⠠⢔⣒⣾⣿⣿⣷⣶⠶⠖⣈⣥⣴⣶⣶⠀⢡⠜⣊⠎⢙⣇⡏⠸⠀⠁⡁⠇⣾⣿⣿⣿⣿⣿⣿⣧⠸⡘⡑⡀⢡⡀⠉⡌⠞⠀⢀⠰⣆⠈⢭⣥⣶⣶⣦⣤⢙⣛⠿⢷⣬⣭⣭⣥⣴⣾⣿⣄⠹⣷⣬⣼⣿⡏⣿⣷⢀⣾⣷⠀⡇⠀⠉⠀⠀⠀⢀⣈⣡⠐⠀⣸⠟⠀⠀⠘⡖⠀⠁⠀⠆⠀⠀⢠⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢸⣿⣿⣿⣿⡇⣿⡅⣿⣿⣿⣿⣷⠀⠀⡌⢄⢻
⠚⠚⠓⠓⠓⠛⠛⠉⠀⠀⠀⠀⣿⠀⡿⠟⣋⣭⣶⢢⡿⠀⠀⠀⠀⠀⠈⠐⠀⠀⠀⢿⠀⠿⠿⠟⠀⠀⠀⢰⣿⣿⣿⣿⣿⣃⠸⠛⢿⠻⠏⠐⠀⠈⠻⢿⣿⡆⠀⡀⠀⣸⠀⠀⠘⣡⣿⣾⣈⣭⡭⣠⢀⣻⣛⣛⡶⠭⠭⠿⠾⠿⠟⣛⣛⣩⣭⣶⣶⣿⣿⣿⠟⢋⣠⡾⠓⠚⠥⢶⣾⠿⠃⠀⠀⠀⠀⠀⠉⠉⠙⠛⠛⠋⠉⠁⠀⠳⠱⠁⠀⠠⣶⠤⠐⠴⠶⣤⣙⠿⣶⣦⣍⣛⣛⣛⣚⡛⣻⣶⣤⣬⣙⣙⣛⠛⡛⠻⠦⢠⢰⣶⡤⠄⣿⣽⡸⣿⠏⢀⡝⣀⠀⠀⠀⠀⡸⠿⠻⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠸⠇⠀⠀⠀⠠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⢻⠈⡛⢿⣿⣿⡇⣿⡇⣿⣿⣿⣿⣿⣴⣀⣿⣟⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢁⣶⣿⣿⣿⣿⠜⠁⠀⠀⠀⠀⠀⠀⠀⠠⣶⣶⣾⣿⣶⣶⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠐⡄⠀⢠⠀⠈⠀⠀⠀⣡⣾⣿⡇⠀⠀⠘⣿⣿⡭⡿⣱⡿⣼⡸⣿⣿⣿⣿⣿⣶⢆⡜⢛⣿⣿⣿⣿⡿⠟⡋⣥⣶⣶⣿⣿⠿⣱⣶⣾⠟⣠⣴⣤⡦⣆⣴⣤⣤⣤⣄⠀⠀⣀⣤⣤⣤⣤⣴⣶⣤⣶⣜⢿⣶⣶⣤⢷⣿⣿⣿⠶⡬⠉⠛⢿⣭⣿⣿⣿⡿⠻⣿⣿⣿⣿⣿⣿⣿⣿⡎⣷⠻⣿⠓⣹⣿⡇⠉⠀⠘⠳⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⣶⣶⣶⣶⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣇⢻⣷⣮⣙⠃⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢃⣾⣿⡿⠛⢋⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⢀⣤⠶⢚⠛⣋⡀⠀⠀⠀⣙⡿⠁⠀⣿⡧⢹⢧⡽⠿⠟⣲⣭⠁⣸⣿⡎⢛⡛⡛⣿⡂⢸⣿⣌⡙⣯⠉⣶⢘⠻⢋⣁⡘⡛⢉⣭⠅⠀⠀⠀⡄⠀⡄⠀⠀⠀⢠⠀⡄⠤⠤⢭⡍⠉⠛⣋⠛⠛⠛⣠⡄⣝⡛⣛⣴⣷⠀⣶⣌⠛⠿⢟⣵⣿⠸⢟⣻⡝⠻⣛⣛⣿⠁⣿⡇⠛⠸⣿⠟⠀⠁⠀⠀⠈⠻⠿⣿⣂⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣷⣶⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣿⣿⣿⣇⢻⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡞⠞⢋⣡⣴⣾⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⡙⠟⠉⠁⠒⠀⠀⠀⠀⠀⠹⡇⠀⡀⠛⢣⣶⠞⡡⠠⣾⣿⢃⠀⢻⣿⠇⠀⣷⡅⠛⡟⠼⠈⢿⣷⣿⢸⠏⣠⠾⢯⡿⢢⢳⣥⣻⣿⡞⢣⠳⡗⡂⣿⠀⣿⢀⢺⠗⢠⠳⣾⣿⠓⣰⣂⢾⣧⡶⣿⡙⠿⢉⢇⡟⠋⢩⠰⡟⠳⣿⡟⡮⣿⣿⠄⠈⢿⣶⡇⢉⠿⣬⣄⢿⠇⢀⢁⢻⠆⠀⠀⠀⠀⠀⠲⣒⠂⢭⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢀⣬⡙⠿⣿⣇⢳⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠤⠤⣤⣤⡄⠀⠀⠀⠀⠀⠀⢀⠐⠻⣿⣿⣿⣿⡿⠟⠂⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⡿⠀⠀⢀⣤⢸⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠊⠋⠙⢷⠉⠛⠛⢻⣷⠀⠀⣀⣀⠁⠈⠉⠀⠘⠋⠊⠀⠓⠀⠀⠘⠀⠘⠃⠘⠀⠂⠤⠆⠃⠃⠀⠘⠟⠙⠘⠼⠵⠚⠩⠶⠾⠇⠉⠁⠙⠀⠀⠀⠂⠆⠺⠀⠩⠘⠎⠀⠆⠇⠟⠃⠠⠱⠿⠠⡭⢛⠾⢷⡆⠸⠸⠃⠀⠸⠀⠏⠀⠙⡟⢰⠘⠟⠠⠸⠎⠋⠡⠤⠱⠝⠿⠈⠀⠚⠀⠘⠀⠀⠀⠀⣠⡤⣤⣤⣬⣼⡷⢿⡇⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣷⣤⡙⠘⠇⠿⠿⠿⠿⠿⠿⠿⠿⠿
⠀⣀⣀⣿⠃⠀⠀⠀⠀⠀⢠⠘⣆⠀⣹⡿⠛⣁⣤⣾⠿⢧⡀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡇⠀⠀⠸⠿⠘⠿⢿⣿⣿⣿⡏⠀⠀⠀⠀⠀⣤⠆⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠉⠉⣀⠰⢆⠲⢿⡿⣿⣷⣾⣿⣿⣶⣤⣅⡀⠀⣒⣠⣶⣦⡤⠤⠤⠤⠤⠀⠀⠀⠠⢤⣤⡶⠃⠤⡭⢭⣭⣽⣇⣠⣆⣘⠻⠀⣾⣿⣦⣦⣴⣶⣦⣴⣙⠃⠽⢓⡀⡀⡀⠀⠀⠀⠀⠀⠀⣀⣤⡤⠄⣠⣤⠤⣀⣀⡤⣴⣾⣶⣤⣤⣶⣶⣶⡤⣤⡤⠤⠴⠷⠖⢂⠀⡸⠅⠉⠛⠞⠋⠀⠀⠁⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡏⣶⠀⠀⠀⠀⠀⠄⢾⡧⠀⠀⠀⠀⠀⠀⢀⠙⠿⣿⣿⣿⡿⠉⠡⢀⣤⠶⠶⢶⣦⢲⣶⣶⣶
⠿⠿⠿⠿⠆⠲⠶⠶⠶⠶⠾⠧⠙⠉⡡⢴⡿⠟⢋⡠⡄⠈⠻⢄⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡇⠲⠿⠿⠿⠿⠿⢋⣿⣿⣿⡇⠀⠀⠀⢀⠸⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠈⢻⣆⣙⣣⣀⡶⡦⢿⡌⣭⣤⣘⣥⣝⣛⣛⣿⣯⣝⣿⣦⢁⣾⣿⣿⣿⣛⣓⣂⣷⣤⣬⣐⡂⢀⣀⣀⣀⣀⣀⣀⣀⣒⣂⣀⢀⢰⣒⣀⣀⣂⣶⣶⣦⣔⣤⣤⣀⠀⢻⣻⣛⣛⡿⢿⣿⣛⣛⣲⣍⡛⠛⢻⣿⣿⣿⣿⣿⣭⣾⣿⠆⠆⠇⠀⠁⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣷⢠⡀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡿⢿⣃⠻⠁⠂⠀⠠⣶⣶⣶⣶⣶⣤⡀⠀⢀⣴⠻⢿⣦⣌⠻⠟⠀⣰⡇⣸⣿⡀⠀⢨⣿⢸⣿⣿⣿
⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⢠⣶⡿⢚⣁⣴⣾⣿⠯⢥⣀⠀⠀⠂⠀⠀⠀⢹⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠠⠀⠁⠀⠀⠉⠙⠂⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠇⠀⠀⣆⣿⣿⣿⣿⣿⣿⠂⡇⣿⣿⣿⣿⣿⣿⣭⣹⣿⣟⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢺⣼⣿⣿⣟⣻⡿⣿⣿⣿⣿⣿⣿⣿⡜⣿⢿⣿⣿⣿⣟⣿⣿⣿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⠕⢋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⣾⠟⠙⠀⠁⠄⠀⠀⠀⠀⠀⢸⣿⣿⡇⣘⡿⠿⠿⠿⠿⠶⢸⣿⣷⣾⣿⣿⣶⡄⣠⡾⢣⣴⣄⣙⠻⣿⣦⣄⠙⠐⠛⠛⠛⠛⠛⠿⠊⢿⣿⡿
⡍⢯⠉⠙⠉⡝⠩⠉⠉⡩⣿⠘⣷⣶⣿⣿⣿⣿⣧⠉⡗⠢⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠆⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠋⠛⠦⣤⣄⣀⣀⣀⣀⠀⢀⠛⣻⠿⠿⠿⣿⣿⠄⠇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡿⣿⣿⣿⣿⣿⣿⣿⣯⠻⢿⣿⠏⡇⢿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢸⣯⣦⣝⡷⠅⢴⣿⣷⣿⣿⡿⡿⠀⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣯⣥⠴⠅⠢⠀⠀⠀⠀⠀⠀⠀⢀⣀⡢⠤⣠⣤⠄⠀⠛⠈⠁⠀⠀⠀⠀⠀⠈⡣⣀⠀⠀⠀⢸⣿⣿⡇⣿⠘⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⠀⠋⢐⣿⣿⣿⣿⣷⣆⣙⠻⢷⢠⣤⣤⣤⣤⣤⣤⣶⣿⣿⣷
⣵⠃⢣⢀⠜⣡⡃⢸⠀⢳⣻⣧⢹⠘⣿⣿⣿⣿⣿⡇⠂⢀⡀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠈⠉⠛⢿⣿⢹⣵⣶⣴⣦⣤⣭⣤⣤⣤⣀⣙⡁⠋⣙⣛⣛⠻⠏⠁⢁⠈⠉⠉⢉⠋⡩⠉⠙⠋⠋⠛⠘⠃⠘⠛⠸⠿⠟⢻⣻⠿⠿⠿⠆⠙⡸⣛⠛⠛⠛⠻⠛⡛⢻⡟⠋⠉⠙⠀⠃⠿⠿⠿⠿⠟⠫⣍⠻⢟⣉⢁⣘⡛⣛⣋⣀⣤⣬⣔⢤⢠⣤⠴⠐⠒⠚⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿⠂⡀⠀⢸⣿⣿⣇⢻⡀⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⠀⠰⣛⠿⣿⣿⣿⣿⣿⣷⠀⢎⣿⣦⣬⢹⡽⢏⣿⣿⣿⣿
⢸⢳⣮⡼⡶⢌⠈⠳⡜⡄⠇⣿⡌⣧⠸⣿⣿⠟⢋⣤⠂⠙⠁⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⠿⠉⠀⠀⠈⠛⢤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠇⡞⠈⠿⢻⣿⣿⣿⣿⣿⣿⣿⡿⢳⡚⢟⣛⡿⢿⠿⠿⠿⠿⠿⠿⢿⡷⡿⠿⠿⠿⣿⡿⣿⣾⣷⣿⣷⣶⣶⡆⣿⣶⣶⣶⣶⣶⣴⣾⣶⣿⣿⣿⣿⣧⢸⡿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣾⣿⠾⣷⣿⣿⣿⣿⣿⣿⣿⣿⣛⠛⠏⠈⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠟⠁⠃⠘⢷⡈⢿⣿⣿⡈⡇⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠪⢿⣿⣿⣿⣿⠏⡜⣸⣿⣷⢻⣌⢸⣿⣿⣿⣿⣿
⠢⠋⠇⠃⠘⠊⠳⠀⠃⠀⠘⠘⣧⠸⡆⢋⣠⣶⡟⠋⠀⠐⣠⡼⠛⠁⠀⠀⠀⠉⠉⠉⠁⠀⠀⣿⣿⣿⣿⡿⣯⡍⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⠦⣤⣤⣶⣆⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⢰⠠⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⡇⣸⢺⣿⣿⣷⣿⣿⣿⣿⣞⣳⣿⢾⢸⡟⢿⡗⡜⣾⣿⣶⡾⣿⣷⣿⣷⣶⡗⣿⢫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣸⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⢿⣶⡇⣿⢹⣿⣿⣿⣿⡛⠿⠫⠁⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣐⣶⣶⣶⠾⠻⠏⠀⠀⠀⠀⠀⣘⣦⣿⢿⣷⣷⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢀⣀⠹⣿⣿⠟⣸⢃⡿⣿⡿⣿⠛⢸⣿⣿⣿⣿⣿
⠶⠶⠶⠶⠶⠶⠶⠶⠤⠶⠶⠶⢿⣆⢷⠸⢛⣵⡄⣴⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠛⠁⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠙⠻⢿⣿⣯⣥⣤⣤⣲⣔⡿⠶⠖⢀⣠⣤⣽⣻⣿⣛⣿⣯⠹⠃⠯⣾⣷⠿⡿⣿⣿⡟⣿⣿⣯⣿⢟⢸⠠⢊⣴⠾⣹⣿⣟⣯⣿⢿⣾⡿⢿⡏⣿⡼⢿⣷⡿⣯⣽⣾⣿⣿⣿⣯⡻⣿⣿⡞⣯⡻⣿⣿⣿⣿⣿⣿⡟⣾⣿⣷⢸⡎⣿⣿⣿⣿⠀⠅⠀⠀⢀⣀⣀⣰⡀⠀⠀⠀⠀⠠⣦⣤⣄⣤⡤⣴⣶⠶⠿⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣻⣿⡄⢸⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠈⠻⣷⣄⡙⣰⡇⣾⠉⠉⠸⠁⠾⢸⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⡈⣻⡟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠸⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠉⢙⢛⠈⢛⣟⣷⣶⣶⣬⣭⣭⣭⣭⣭⠉⠛⡥⣀⠚⠿⠿⠷⠿⠿⠟⠫⠜⠸⠰⠿⠿⠉⠈⢨⢩⠹⠿⢿⣿⡛⠀⠂⠛⣘⣛⣛⡛⡛⢫⢹⡗⠉⢋⣟⣁⡽⢉⡁⣿⣿⣝⣏⣙⣋⣯⠩⠰⣍⠿⠿⠖⠶⠿⠿⢛⣛⣛⣻⣿⣿⡷⢶⣿⡾⠟⠻⠟⠛⠿⠟⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠿⠄⠈⢿⣿⣿⣿⣿⡿⠀⠀⠈⠉⠉⠉⠉⠀⠀⠘⢷⣤⠀⢀⡙⢃⡿⢸⣷⣶⣶⣶⣶⣶⢸⣿⣿⣿⣿⣿
⠒⠒⠒⠶⠶⠶⠶⢶⣶⠶⠶⠶⠶⠶⠶⠈⠟⣉⣤⣤⣶⣤⣤⡀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠈⠑⠀⢠⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠿⣿⣶⣶⣿⣶⣦⣽⢉⣡⢲⣶⢠⡛⣿⡿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡇⡾⣿⠿⣿⣿⣿⣿⣶⣶⣾⣿⣿⡿⣿⣾⢸⡿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡶⣶⣿⣿⣿⣿⠆⢙⢛⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡏⠀⠀⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⠀⠀⠀⠀⠀⠀⠀⠄⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣛⣅⡶⢡⣶⣶⣶⣶⣶⣶⣶⠸⣿⣿⣿⣿⣿
⣀⣄⣀⣤⠀⢠⣤⣿⣿⣥⣴⠄⣠⢯⣤⣤⣶⣿⣾⣿⣿⣿⣿⣿⣿⣷⣦⣄⣀⡀⠀⠀⠀⢀⣀⣐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠷⠶⣶⣿⣷⣤⣀⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣾⣿⡇⡎⠸⣷⣿⣿⢻⡿⣶⣶⣾⣷⣾⣿⣿⣿⣷⣿⣿⡇⣇⢛⡶⡟⣧⣶⣶⣿⣷⣶⣷⡖⡾⣈⢠⣸⣿⣺⡷⣶⣾⣿⣿⣿⡷⣾⣾⣿⣷⢾⣿⣷⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣤⣤⣶⣶⠿⠟⢻⡇⠀⠀⠀⠀⠀⣀⡀⠀⣀⣬⣧⣬⣕⣒⣀⣄⣀⠀⠀⠀⠀⠀⠈⠛⠱⠛⠛⠛⠛⠛⢛⣛⡛⠐⣿⣿⣿⣿⣿
⠤⣤⣾⣿⣿⠟⣿⣿⢿⣷⣶⣾⣿⠿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣷⣿⣿⣿⣶⣦⣀⣤⣤⣴⣾⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠷⣿⣶⣿⣿⣯⣶⣶⣶⣤⣤⣤⣄⣀⣀⣀⠀⢿⡿⠿⢿⡿⣿⣿⣿⣿⡇⡇⠀⣟⣿⣿⣋⣾⣾⣿⣿⣟⣼⢻⣥⣭⠚⢻⣿⡇⡏⢀⡻⠾⣿⢿⣛⣷⣖⡛⢿⣞⠈⢀⠈⢸⣿⣾⠳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣛⣿⡿⠂⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⠄⢻⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣤⣤⣴⣿⣿⣿⣿⠙⡟⠛⠉⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⣼⣯⣻⡿⣷⣂⠢⢵⣷⣾⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣻⣿⣿⣿⣿
⠶⢿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢟⣧⣤⣤⣤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠉⡬⠛⠛⠻⠿⠿⠿⠿⣿⣿⣿⢛⠡⣐⣻⣛⣓⣲⢶⣶⣶⣦⣥⣬⣭⣟⣛⣿⣿⡛⣛⢛⢛⣛⣛⣛⣛⣛⣉⣚⣃⣃⣀⣀⣚⣋⣒⣙⡛⣛⣒⣉⣛⣀⣂⣘⣹⣿⣈⣛⣛⣛⣛⣛⣛⢻⠛⡛⣛⣛⣛⣛⣋⣀⣀⣿⣿⣯⣭⣭⣤⣤⣴⣦⣴⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⡿⠻⢿⡛⠛⠋⠙⠗⠒⠛⠛⠉⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣷⣤⣌⣉⣛⡿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣷⣶⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣧⣤⣶⣿⣿⣿⣿⣿⣿⣯⣿⣿⣶⣶⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀⣲⢿⡖⡌⢠⣝⠻⣿⣛⣛⠻⡿⠿⢷⣿⣿⣿⣿⣿⣿⣓⣾⢱⣿⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣇⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣿⣿⣿⡿⠿⠿⠾⠋⠈⠉⠀⢀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣤⣴⣶⣤⣄⡉⠉⠉⠙⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣄⣛⣯⡭⠿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⠿⣿⣿⣾⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣶⣶⣤⣤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠇⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣶⣶⣾⡿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣷⠿⠷⣿⢨⣭⣭⣭⣿⣿⢿⣿⣭⣽⣿⣿⣯⣿⣾⣭⣭⣭⡅⣸⣿⣭⣭⣭⣝⣳⣶⣦⣭⣵⡶⣶⣶⡶⣾⠇⣿⢨⡿⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣠⣤⣴⣶⣾⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣬⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿''', 0.5)
def jimmy_art():
    echo('''⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⢟⣿⣿⣿⣿⣻⣾⣿⣿⣿⣿⣿⡿⣽⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣟⣽⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⡿⣿⣿⣿⣿⣿⢏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣷⣿⢿⣿⣿⣿⣿⣿⢯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣟⣼⣿⣷⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠽⢆⣸⣿⣭⣟⣛⣛⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠐⢄⠐⠭⢾⣧⢻⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣼⣷⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠘⠟⡀⠃⡼⣯⣶⡼⢿⣯⡙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣿⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢫⣾⣿⣿⣿⣿⣼⣿⣽⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⢳⣧⢴⣬⣻⡿⢿⣀⣝⠻⠆⠻⢽⢻⡞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⡟⢡⣾⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⡨⢸⣾⡿⠿⣾⣤⡛⢿⣿⣿⣷⣾⣯⡄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⡿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⢠⣿⣾⣧⣞⣺⣶⣽⣿⣿⣷⣷⣷⠶⢶⣯⡘⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⣿⢯⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⡇⣾⣧⡄⢠⣧⣸⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣵⣻⣿⢾⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⡿⠏⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⡇⣿⣿⣇⡼⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⢿⣿⣿⣿⣿⣿⣿⡇⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⡷⠸⣿⣼⡇⣿⣿⣿⣿⣿⣿⣿⡿⠟⣛⡀⣿⢏⣽⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⠀⠘⠿⠇⣿⣿⣿⣿⣿⣿⡋⢀⡴⣭⣽⣯⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣷⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⢀⠂⢸⠹⠛⠙⡛⠋⠡⢸⣿⣝⣻⣿⣿⣿⣪⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢺⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣓⣶⣿⣷⣶⣶⣶⣶⣶⣶⣶⣮⣬⡻⠿⣿⡿⡿⠙⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣻⣿⣷⣮⡻⠃⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣛⣉⣉⣉⣅⣈⡓⠦⣝⣯⣅⡻⣿⣿⣿⣿⣿⣿⣿⣯⣟⣿⣿⣿⣦⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣸⣿⣿⣿⣿⣿⢷⣿⣿⣿⣿⢿⣷⣽⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⠏⡴⠿⠿⠿⠿⣛⣫⣯⣟⣛⣛⡛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣙⠻⣿⣉⣋⣛⣻⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣯⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢿⣿⣿⣿⣿⢩⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⡿⣼⣿⣿⣼⣿⣼⣿⣾⣿⣿⣿⣿⣿⣯⢿⣿⡿⠃⠀⣠⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⠿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠙⠷⢤⣉⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⣿⣿⣿⣿⣿⣿⠇⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠟⢛⣛⣉⣙⢮⢻⣿⣿⣿⣿⣿⣿⣶⣤⣀⣀⣺⣿⣿⣶⣤⣀⠙⠛⣿⣿⣿⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⡏⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⢉⣾⣿⣿⣿⣿⡿⣾⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⡟⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣴⣶⣾⣿⡿⠿⠿⠿⣿⣷⣍⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣄⡙⠿⣿⣿⣿⣿⣿⣞⢿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣭⣥⣶⣶⣶⣶⣿⣿⣿⣿⣿⣹⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣝⡿⣿⣿⣿⣯⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⠏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣾⣿⣿⣿⣿⡟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢠⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡄⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⣽⣻⢿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣿⢿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣱⣿⣿⣿⢿⣿⣿⣟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⣉⡇⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣝⣻⡿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣃⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⢶⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⠁⡠⠖⢋⣀⣈⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣥⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⢻⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣾⣿⣿⣿⣿⣿⣿⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⡡⠤⠐⣀⣴⣶⣿⣿⣿⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⠗⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣼⣿⣿⣿⣿⣿⣿⢯⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣟⣾⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣜⣿⣿⣿⣾⣿⡿⣿⣿⣿⣿⣿⣿⡏⣼⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣯⣭⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⢋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⢡⣿⣿⣿⣿⣿⣿⣿⣾⣿⣾⣿⣿⣿⣿⣻⣿⣿⣿⡿⣿⣿⡾⣿⣿⢹⠻⢁⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣶⣭⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⡿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⢧⣿⣿⣿⣿⣿⣿⡿⣼⣿⣏⣿⣼⣿⣿⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⡇⠀⣧⢮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⡻⣮⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣱⣿⣿⣿⢸⣯⣿⣿⣿⣿⢸⣿⣿⣿⣿⣾⣿⣿⡇⠀⠽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣽⠟⠛⠻⢿⠎⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣹⡇⣿⣿⣿⣿⣿⢹⣿⣷⣿⣿⣿⣯⣿⣿⣿⣿⣿⣷⠀⢸⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⡾⣵⣾⣿⣿⣿⣿⣷⣿⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢾⠯⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣳⣿⣧⣿⣿⣿⣿⣿⡼⣿⣿⣿⣿⣿⣹⣧⣿⣿⣿⣿⣻⣧⠀⠳⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⡞⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣽⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣳⣿⣿⣿⣿⣿⣿⢷⣿⣿⣯⢿⡇⣿⢿⣿⣿⣻⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⡿⣧⣌⠛⠟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣯⣿⣿⣿⣿⣟⣿⢣⣾⣿⣿⣿⣿⣿⣿⡾⣿⣿⢻⣇⣿⣻⣷⢻⣷⣟⣿⡿⣿⣿⣿⣾⣿⡿⣦⡀⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⠿⣿⣿⣿⣿⣿⣷⣾⣿⣽⣿⣻⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡗⣿⢻⣿⣿⣿⣯⣿⢿⡟⣿⣽⣷⣿⣿⣿⣿⣟⣿⣿⣿⣄⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣾⠸⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣟⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣏⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣟⠫⠭⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣾⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣽⠈⠙⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣶⣿⣽⣿⣿⣿⣭⣿⣿⣿⣿⣿⣿⡿⢿⣿⣷⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣵⣿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣷⣿⡿⣿⢿⣏⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣻⣿⣿⠆⠀⠀⠀⠀⠀⠀⠈⠙⠿⣿⣷⣆⠀⠀⠀⠀⠀⠉⠙⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣟⣿⣿⣟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡿⣿⣿⣿⣽⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣧⣿⣿⣽⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠃⠀⠀⠀⠀⠀⠀⠀⠐⠒⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡻⣿⣿⣿⣿⣮⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣭⣭⣛⣛⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣶⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣽⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣾⣍⢿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣥⣷⣶⣤⣤⣤⣾⣽⣿⣿⣿⣿⣯⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⣋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⢿⣿⣿⡇⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⡻⢿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣷⡝⢟⠽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⢳⣿⣼⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⢾⡇⣿⣿⣿⣿⣿⣿⣷⢿⣿⣿⣿⣿⣟⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣇⠈⠛⢿⣿⣿⣿⣿⣷⣬⡛⢿⣿⣿⣿⣿⣷⣝⠻⣿⣿⣿⣿⣿⣽⣿⣿⣿⡦⠀⢻⣿⣿⣿⣿⣿⣿⣿⠀⢲⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣷⣼⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣹⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣽⣤⡀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣶⣶⣶⣶⠀⣐⣿⣿⢏⣿⣿⣿⣿⣿⣿⣿⣿⣷⡆⠉⠛⠿⣿⣿⣿⣿⣷⣬⡻⣿⣿⣿⣿⣷⣮⡙⢿⣿⣿⣿⣷⣍⠛⠁⠀⢹⣿⣿⣿⣿⣿⣿⠆⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⠀⠀⢌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣦⣍⠛⢿⣿⣿⣿⣶⡈⠻⢿⣻⣿⡃⠀⠀⣪⣝⣻⡿⣿⣿⠏⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠜⠈⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣄⠙⠻⣿⣿⣿⡦⠀⠈⠉⠀⠀⠀⠛⣿⣿⣿⠎⢀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣟⣿⠿⠿⣿⣿⣷⣿⣭⣟⣛⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣻⡏⣿⣿⣯⣿⣿⣿⣽⡿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣧⢘⡇⣟⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⠭⠭⠃⢀⣀⣉⢉⣥⣴⣶⣆⠀⠀⠀⠀⢺⣿⣷⡆⣿⣿⣟⢙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣯⣟⣿⣶⣄⣈⣿⣿⣽⣿⣿⣿⣝⢿⣿⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⡿⣿⣷⣿⣿⣿⣿⣾⣿⣹⣿⣿⣿⢿⣿⣿⣿⣿⣿⢘⣧⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⢀⣰⣶⣶⣆⢈⠀⠀⢀⣵⣻⣿⣿⣿⣾⣿⣿⣿⣄⠀⠀⠀⠸⢿⣷⡇⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡿⣮⣣⣿⣿⣿⣿⣿⣷⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣼⣧⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠐⠿⣿⣿⣿⣿⣤⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢸⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣽⢯⣾⣿⢿⣿⣿⣿⣿⢿⣿⣹⣷⣿⣿⣿⣿⣿⣿⣿⣿⠨⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⠛⡛⠳⠄⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣾⣿⣿⣟⣿⣸⣿⣿⣼⣯⢿⣽⣿⣿⣿⣿⣿⣿⣿⣿⡇⢹⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠻⣿⣿⢻⣀⣥⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢟⢛⣿⠇⠀⠀⠀⠀⠀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠈⠙⠛⢿⣿⣿⣿⣿⣿⣾⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡿⣿⢟⣽⢿⣯⣏⡿⣻⢆⢪⣿⣿⢟⣺
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⢿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣷⠀⢿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣮⣌⣠⣾⣿⣿⣆⠀⠀⠈⠏⠉⠹⢿⠙⠿⡩⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⢿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣷⣾⢟⣿⣟⡻⢛⣿⣟⣟⣽⣿⣾⣿⣇⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣻⣿⣿⣟⣽⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣇⠨⢿⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠈⠀⠁⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣆⡀⠀⠈⣻⣿⣾⣿⣿⣿⣿⣿⣿⣿⣏⣯⣽⠟⢽⡛⠫⡿⣡⣿⡟⢟⣿⣾⡿⣫⣾⣿⣿⣽
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣷⢿⣿⡿⣵⣿⣿⡟⣾⣽⡿⣿⣾⣿⣯⣾⣿⣿⣿⣿⣿⠀⠊⢛⠿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣻⣿⣶⣶⣧⣿⣿⣯⣿⣿⣿⡿⢿⣯⣼⢽⣭⣕⢕⣾⡿⣿⡿⣿⣿⣿⣿⢻⣳⣿⢿⣯⣍⣽
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣾⣼⣿⣿⣏⣶⣶⣾⣿⣿⣻⣟⣾⣿⣿⣿⣿⣿⡆⢀⠀⠀⠀⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢀⣀⣈⠻⠿⣿⣿⣟⣿⣻⣿⣿⡷⢹⣿⣿⡟⠫⢴⡝⣅⣛⣛⠋⣻⣿⣏⣧⡾⡿⣺⣿⣿⣳⢾⣿⣿⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣻⣯⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣿⣦⣝⣓⣦⠤⠀⠀⠈⠉⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣀⠀⢐⣿⣿⣿⣿⣷⣶⣭⣛⠻⠛⠻⢿⣟⢾⢿⡵⣕⣿⢏⣵⣟⢟⣧⣾⡿⣽⢿⢟⣻⣽⣯⣽⡷⣫⣻⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠂⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣺⣿⣻⣗⠏⣝⣾⢗⣾⣾⣿⢿⣵⣷⣿⡾⣿⣿⢿⣽⣿⣵⣿⢽
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣉⠉⠉⠈⠩⠉⠍⣹⣿⣿⡿⠿⠿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡘⡟⢁⣻⣾⣟⣿⣻⣿⡿⠷⢋⣲⡟⢣⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣾⣯⣉⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠐⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣭⣬⣯⡷⣃⣾⣿⣿⢩⣾⠿⢻⣾⣟⡫⣿⣻⣿⣭⣽⣻⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣻⣿⣿⣿⣿⣿⣷⣶⣶⣤⣄⡀⠀⠀⠐⠈⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠘⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣯⣯⣴⣿⡿⢏⣴⣿⣿⣧⣽⣿⣿⣣⣾⣿⢯⣽⣿⣿⣿⣽
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⢋⣤⠦⠉⠉⠙⠛⠻⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⣰⡄⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣶⣿⣿⣿⣗⣷⣾⣟⠟⢫⡿⣻⡿⣿⣿⣟⣋⣿⣯⣿⣿⣏⣻
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠤⠀⠈⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠹⠿⠛⠛⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠘⢿⡟⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠚⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⡿⣽⣼⣾⣿⢗⣦⣾⣿⣿⣿⣿⣿⣿⣻⣿⣿⢿⠿⠿⣿⣟''', 0.5)
def rat_art():
    echo('''⣿⣿⣿⣿⣿⣿⣿⣿⣟⣽⢿⢿⣿⣿⣿⣿⡿⠛⣠⠿⠿⣿⣿⣿⡿⣿⠏⣿⣿⣿⡿⣿⣿⣿⣿⣿⡻⢻⡿⢻⡟⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣾⣿⣾⣃⣁⡀⣠⣿⢟⣿⠖⣴⣿⣿⡿⠙⢰⣿⣿⣿⣿⣿⣷⣼⡟⣾⠃⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⠻⢿⠇⣹⣿⣿⣡⢾⢏⠎⣥⣿⣿⢿⣷⢠⠛⠀⢿⠟⢙⢛⣯⡿⠇⡆⡇⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⡷⣟⣻⣭⣽⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⣿⣄⣿⣿⣆⡙⡼⡼⢿⡇⣱⡦⡸⣿⣷⣿⠤⣿⣷⢠⢂⣠⠠⣾⡿⡛⠽⣇⣴⠇⡅⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠀⣾⢡⡻⢿⡿⢃⣻⢷⣀⣼⣽⣾⣿⣿⣿⡿⣧⡿⠿⢿⣿⡿⣼⣿⡿⢦⢠⣾⡿⢿⡇⣸⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣯⣿⢣⣼⢡⣻⢿⣿⣯⡿⣿⣿⣿⣿⣟⣾⢟⣾⢏⣿⡿⢠⣟⠛⢻⣞⣽⣿⣿⡿⣹⣿⡏⣾⢻⣷⡻⣿⣿⣿⣿⣿⣿⣿⣿⣛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣿⡿⠃⢾⣼⢘⣿⣿⣷⣽⣿⣿⢩⡿⣗⣯⣾⣿⠿⣵⣿⣿⣿⣊⣻⣿⣥⡟⣱⣿⣿⡇⢳⣞⢿⣱⣿⣿⣷⣝⢿⣿⣿⣿⣿⣿⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⠟⢯⣷⢸⡏⢰⣿⢿⣿⣏⣼⢏⣧⣟⣭⣿⣟⣿⣿⣿⣽⣿⣿⢿⣿⣹⣿⡟⣅⢿⣿⣿⣧⡀⣧⡄⣥⣿⣿⣿⣿⣿⣮⣛⣿⣿⣿⣿⣎⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡿⣼⣳⢻⡟⠸⠟⢸⣿⡸⢟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣵⣿⠟⢐⣿⣾⣟⣿⣿⡷⢸⢣⣟⣿⣿⣿⣿⣿⣿⣿⣷⣟⢿⣿⣿⣷⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⢋⣾⠟⣚⡟⠃⡇⢱⣧⡇⠈⣟⣽⡛⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣗⣿⣳⢠⢸⣿⡟⣿⣿⢿⣷⣸⡛⣛⣿⣾⣻⣿⣿⣿⣽⣿⣿⣿⣟⢿⣿⣿⣷⣝⣻⣿⣿⣿⡟⣿⣿⣿⣿⣿⣎⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣟⣵⡾⣁⣾⠛⣾⡯⠐⣎⣄⣿⡽⠃⣼⡿⣿⣧⣭⣟⣿⣿⣿⣿⣿⣻⣿⣿⣿⡿⢣⣿⣼⣟⣥⣿⣿⣼⣿⣿⣷⣿⢳⣎⣽⣯⣽⣿⣿⣿⣿⣿⣿⣿⣿⣓⣾⣿⣟⣿⣿⣿⣿⣾⢿⣿⣿⣿⣿⣶⣝⣿⣿⣿⣷⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⢛⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⠳⣶⣿⠁⠂⡞⢹⢟⢁⣼⣿⣷⣟⣷⣾⣿⣿⣿⣿⣾⢻⣿⣿⣿⣿⢁⣿⢻⢻⢻⢻⣿⡇⡿⣻⣿⣿⡟⣎⢿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣶⣟⣿⣶⣿⣿⣿⣤⢿⣿⣿⣿⣿⢳⡽⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠉⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣛⣯⣭⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢳⣿⣾⣿⢇⣀⠈⠈⣸⠇⣼⣧⣮⣿⡟⣱⣿⡿⣿⡶⣸⣻⣿⣿⣿⣿⢏⣾⣿⣿⣾⡆⣾⣿⣷⣧⣿⠏⣿⣿⣿⣷⢯⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡿⣿⣿⢾⣿⣿⣿⣿⣷⣿⣿⣷⣾⣯⣉⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⡿⠋⡴⠿⠸⠃⢁⣼⣿⣿⣿⣿⣿⣿⣿⣇⠀⠿⣷⣿⣿⣿⣿⢋⢸⣿⢹⢿⣿⣹⣿⣿⡏⣾⣯⣴⣿⣿⣿⣿⣿⣿⣶⣭⣛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⡿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣫⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣯⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡿⠿⣿⠅⠃⢁⣤⠁⠰⠑⠠⣾⣿⣯⣾⣿⡿⢻⣿⠇⢨⢀⣖⡿⣿⢿⣯⣤⢯⣽⣟⣾⣾⣧⣿⣿⣿⢧⡿⢹⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠒⠙⠀⠀⠈⠈⠉⡆⠀⠀⣀⠀⠀⠀⠈⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣷⣿⢃⣠⢿⠋⡀⣀⣴⣿⣿⣿⣿⣿⠏⣀⣜⣿⣴⢧⣿⣿⣿⢿⣿⡟⣿⢰⣿⣇⣿⣿⢸⣿⢿⡏⢸⢷⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠁⡠⠈⠀⠀⠀⠀⠀⣤⢤⣠⠋⠁⠀⠀⠀⠀⠀⢈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣡⣾⣿⣿⣿⣿⡟⣿⣿⣿⣿⡿⠿⣫⣽⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣟⢟⣃⠾⣿⡏⣠⣿⣿⢿⣿⣿⣿⣿⠏⢈⣽⢡⡿⣿⣯⣿⣿⢿⣿⡿⡀⣿⣾⣿⢸⣿⣷⣿⣧⣿⡟⡾⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣯⣀⠀⠀⠀⠄⠀⢀⡀⠀⠘⣿⠂⠀⠀⠀⠀⠀⠀⠂⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣭⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢑⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⡸⢿⢝⣿⣿⣿⠾⢯⣼⣿⣷⡿⠛⢳⢾⣷⣿⣿⣯⠕⣾⡟⣼⢸⣿⣿⣧⣿⣿⢻⣿⣿⢿⣇⣇⣿⣿⣇⡟⣿⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⠟⡛⠛⠛⢛⣟⠛⠀⠀⠀⠀⠀⠀⠀⠐⢂⣥⣤⡴⠂⢤⡄⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢫⣼⢿⣵⣿⣿⣻⣿⡿⣋⣼⣿⣿⣿⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣛⣥⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⢃⣃⠟⠨⣿⣿⣠⣤⢀⣾⣿⣿⣽⣾⡿⣻⣧⡿⣷⡟⣼⡟⣼⣿⣿⣿⣿⣿⢹⡟⣾⣿⡇⣿⣿⣿⡿⣿⡏⣧⣿⣝⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⠱⠊⠛⠛⠟⠉⠀⠁⠀⠀⠀⢰⠀⠀⠋⢠⡶⠁⢉⠀⠂⠈⠁⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⠟⣿⢿⣿⣿⣿⣯⣩⣾⣿⣿⣧⣭⡍⣿⣿⣿⣿⣿⡿⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣡⠟⣯⣽⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣇⣿⣿⣄⠒⢿⣿⣿⡇⢸⣿⡿⠿⣣⡟⣽⣿⣟⣽⣯⣿⠃⣸⣿⣿⣿⣿⣿⣟⣿⣷⣿⣿⡇⣿⣿⣿⡇⣿⣇⣿⣻⣿⣧⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣯⡿⠃⢀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠲⠀⠀⠄⠀⠀⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢿⡦⣵⡿⢟⣿⣿⣿⡟⣿⡧⢛⣿⡿⣸⣿⣿⣿⣿⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣧⣬⣛⠟⣉⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣏⣿⠀⣦⣾⠙⠟⣻⣿⣿⡇⠀⢹⡿⡿⡗⣞⣽⣟⡧⢈⣿⣿⣿⣿⣿⣿⢹⣿⢸⣿⣿⣾⣿⣿⣿⡧⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣿⣭⣿⣭⣶⣛⣯⡿⠃⠀⠮⠥⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⣿⣿⣿⣿⣯⣵⣿⣟⣴⣿⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣄⣿⣣⣟⣿⣟⡿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣟⣿⣿⠃⠀⣭⣾⣷⣾⣿⣿⢿⣷⢬⣿⠇⢃⣼⡟⣷⡿⢱⣿⣿⣿⣿⣿⢱⡿⣿⡯⣾⣿⣸⣿⣿⣿⣿⢻⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠛⠉⠁⠒⠛⠛⠻⠇⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⣀⣠⡄⠰⠀⠀⠀⠀⠀⠀⠀⠀⠄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⢏⣛⢧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣏⣴⣿⡿⢃⣵⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⣷⣣⣾⣿⣿⣿⣿⣜⣿⣠⢝⢵⢇⢀⣿⡿⣿⣿⣃⣾⣿⣿⣿⣿⣿⣿⢸⣿⢸⣿⣷⣿⣸⣿⣿⡇⣿⣿⣿⡿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠄⣂⣤⣘⡀⠀⣦⣈⠒⠂⠂⠁⠁⠀⠄⠴⠋⠀⠀⠹⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡋⠾⢟⣶⣼⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣨⣯⡿⢣⡞⣿⣿⣿⣷⡿⠳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣥⣠⣿⣛⣉⣛⣿⣿⣾⡟⠋⣸⡼⣫⣾⢏⣾⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣼⣟⣼⡇⣿⣿⡏⡆⣿⣿⣿⡏⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠊⠂⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢋⣻⣿⣿⣿⠟⣩⡤⢄⣤⠆⠀⠀⢠⡀⠀⠀⠈⠰⠸⠟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣵⡾⣛⣿⣿⣏⣿⡿⢁⣴⡿⣫⣿⠂⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⣿⣿⣟⣷⠟⣸⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⡿⠈⣼⣿⢉⢴⣼⢋⣾⡿⣿⣾⡳⣧⣸⣿⣿⣿⣿⣿⣿⣿⢫⣿⣿⣿⢻⣿⣧⣿⣿⣿⣇⣿⡿⣿⡇⣿⣟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢷⣯⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠐⠀⠀⢁⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠒⠀⠂⠀⠀⠀⣴⣦⡸⣿⢇⡅⠀⢀⠤⠅⠂⠑⠀⠀⠀⠀⠀⠀⠀⠀⠂⣠⠠⣛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣋⣾⣷⣷⣾⣿⣿⣿⣿⣿⣷⣿⠛⡱⣿⣿⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⡿⣯⣿⡷⣣⣟⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣢⠿⠛⢁⣻⣿⣻⣾⢏⣽⣿⠟⣹⡿⣻⣿⣿⣿⣿⣿⣿⣿⣾⣿⣼⣿⣾⣿⢻⣿⣿⣻⣿⣿⣧⣿⢸⣿⣿⣷⣮⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡟⣿⢻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣁⣀⡀⠀⠐⡂⠠⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⣾⠖⠁⠀⢠⠓⠂⣀⢋⣭⡁⠅⠊⠀⢰⡖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠈⠿⠇⠨⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣟⡟⢟⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣷⡿⣫⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣩⣾⢇⣾⢯⣼⢟⢁⣼⣽⠯⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣿⣿⣿⣿⢹⣿⣸⣿⣏⡇⣿⡇⣿⣿⢸⡇⣿⣿⣿⣿⣿⣽⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⢻⡟⠉⠁⣼⢠⣄⣠⡬⣆⡐⠶⠀⠀⣀⠀⢀⡠⠄⠚⠋⢠⡟⠀⠀⠀⠀⠀⢈⠛⠏⠉⠀⠀⠀⠀⣠⠴⠄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠇⠀⠀⠀⠀⠀⠀⠀⣢⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⡿⠏⣛⣁⠚⣉⣉⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⠿⢿⣿⡿⢋⣾⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⠾⣽⡿⡹⢣⣼⣿⣯⢴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣾⣿⣿⣿⡿⣼⣿⢹⣿⢻⡷⣿⣿⣿⣿⣾⣷⣿⣿⣿⣿⣿⣿⣷⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⠿⢩⣾⣿⠷⠿⠿⠷⡶⠿⣿⣿⣰⣷⡁⡨⠀⠠⠨⠁⠘⠛⠄⠀⠀⠀⣾⣇⠀⠀⣤⢠⣤⣾⣿⣇⢀⣴⠿⠾⠮⠑⠀⠀⢀⡄⠀⠀⠀⠀⠀⠀⠁⠀⡀⠀⠀⠀⠀⠰⠀⢸⡿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⠿⣿⣿⣿⣿⣶⡿⢟⣉⣥⣔⣶⣿⢡⣿⣟⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⡿⢘⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢨⣾⣿⡨⢁⣾⡿⡿⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢧⣿⢻⣿⣿⣿⣿⢻⣿⣿⣿⣷⡿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣽⢿⣿⣿⣮⡻⢿⣿⣝⢿⣿⣿⣿⣷⣿⣿⣿⣿⣍⣿⣿⣿⣿⠟⠟⠁⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡽⠛⠟⠛⠻⠿⢷⡄⠀⠀⠀⠀⠠⠦⢾⡿⢲⣤⣾⣿⣘⣧⣾⠿⠝⠉⣉⠦⢀⢠⠄⣼⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠂⡄⠸⠇⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠷⢽⣿⣿⣿⠟⣡⣿⡿⢿⣿⣿⣷⣥⡾⠍⣿⢹⣿⣿⣯⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣯⣽⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣴⣿⢟⣼⢃⣾⢿⢬⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣾⣿⣿⣿⣿⢹⣿⢸⣿⣟⣹⣿⡇⣿⣿⡏⣿⡽⣿⣿⣿⣿⣿⣧⡹⣿⡜⣿⣎⢿⣿⣯⣽⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⡍⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⣆⠀⢲⣀⠀⠀⠀⠀⠀⠀⠀⠁⢀⣴⣷⠐⣩⣟⠻⡿⣿⠿⠛⠻⠿⠿⠀⠰⡠⠀⣿⢡⡨⠉⠀⠉⢀⠆⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠆⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣟⣟⣵⣿⣿⣧⣸⣿⣿⣿⣿⠋⢨⣿⣸⣿⣿⢟⣵⣶⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣿⠿⣿⣿⣿⣿⣿⣿⣿⣝⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢿⢿⡿⣯⣾⢿⡼⢻⣿⣿⣿⢿⣽⣿⣿⣿⣿⣿⣿⢏⣤⢶⣿⢿⠟⣿⡿⢸⣿⣼⣿⣿⣿⢿⡇⢹⣿⣿⡿⣿⣿⣿⣿⡙⣿⢿⣿⢻⢟⢸⡏⠇⣿⣿⣿⡿⣿⣿⣿⣿⣿⡇⣿⣿⡿⠋⠀⠀⠀⠀⠐⠀⠂⡀⠀⠂⠀⠀⠀⠀⠁⠀⠀⠀⠐⠀⠀⠀⣤⣾⣿⣿⡇⠷⢻⠃⢛⠣⠄⠀⠀⠀⠁⠈⠁⠀⠀⢏⣀⣆⣠⠆⠀⠀⠀⠀⠚⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡿⣿⣿⣿⣿⣿⣿⣿⠟⠁⢠⢾⠟⣿⣿⣽⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⣿⠽⣻⣥⠾⠋⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣾⢿⢻⢿⣼⡿⢻⣶⣿⣾⣿⣿⣿⣿⣿⣯⣿⣾⣿⣼⣿⣿⣸⣿⣿⣿⣷⣿⣿⣿⣏⣾⢧⡘⣇⣿⣿⣿⣿⣿⣿⣻⣿⣷⢻⣿⣷⢸⣿⣦⡸⣿⣿⣿⡿⣿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⣠⢱⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣀⣴⣿⣿⣿⣿⣽⣇⠈⠋⠝⣽⣿⠃⠀⠀⠀⠀⠀⠀⠀⢠⡈⠋⡈⠓⢒⡉⠂⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢳⡧⣿⡿⣿⡞⠿⣩⡶⣀⣤⣾⣷⣸⡿⠻⣛⢿⣾⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⠿⣿⡕⣿⣿⣿⣷⠿⢛⡥⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⡿⣷⢿⣼⣵⣿⢾⣻⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⢻⣿⣷⣿⢹⣿⣎⢷⣾⣧⣿⣿⣿⣿⣿⣿⣿⣿⣷⣹⣿⡎⣿⣿⣿⣮⢿⣿⣿⡇⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠄⠀⢁⠠⣘⣀⡀⠀⠀⣀⣀⣠⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠁⠰⠃⠀⠀⠙⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣷⣕⣿⡶⠿⠟⣱⣿⣿⣿⣯⣍⢦⣿⣿⣏⠝⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢽⣾⢿⣿⡇⠿⢟⡿⣢⣵⣯⣿⡛⠿⣿⣽⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⣿⣟⣿⣯⠟⣿⡿⣻⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣼⣿⣿⢸⣿⢸⣿⣿⢋⣾⣿⣿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡜⡹⡿⣿⣷⡆⠙⣁⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⣿⣿⡿⠛⣵⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣻⣿⣷⣾⣿⡿⣯⣽⡹⢁⡈⣟⡙⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢩⣬⣿⣿⣻⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⣣⣿⣦⣿⡅⣻⣿⣿⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⣿⣿⣿⠿⣿⢿⣾⣿⣾⢟⣵⡿⣿⣿⣿⣿⣠⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣾⣿⣟⢿⣿⣿⡖⢁⢆⠀⠀⠀⠀⠀⠀⠀⢀⡀⡀⠀⠀⣾⣿⣿⣿⣿⣿⣿⡗⣱⣗⣾⡿⣛⣲⣶⣦⠉⣋⡹⣠⣽⣻⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠠⣿⡏⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⡯⣼⣿⣿⣿⡆⠁⢻⣧⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡶⣰⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⣧⣿⣿⣿⣿⣿⣿⣼⣿⣿⡟⠻⣿⢻⣿⣿⣿⣿⣿⡷⣿⢏⣶⣿⣿⣿⣿⣾⣿⢼⣿⣫⣿⣿⣿⡟⢿⣿⣿⣿⣇⣜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣯⣻⣾⡿⠋⠎⠀⠀⣷⣤⠉⠀⠀⠀⠀⢹⣿⠃⠀⣸⣿⣿⣿⣿⣿⣿⡿⣸⡿⢘⣯⣾⣿⣿⡿⣋⡼⣛⣺⣿⣿⣿⣷⣾⣿⠀⠂⠒⡀⠀⠀⢀⣄⣄⡀⢐⠀⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⡆⣀⣷⠃⠀⠀⠀⠀⠐⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣻⣿⣹⣿⣿⣿⠿⣯⣾⣷⣟⣛⣿⣿⠖⣼⣿⣿⠹⣷⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣙⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣧⣾⣿⣿⣿⣿⠀⢹⣿⣿⣿⣀⣤⣽⣼⣿⣿⣿⣿⣿⣧⡄⣿⣿⣿⡏⣿⢃⣿⣿⣿⣗⢿⣿⣿⣷⣿⣾⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⣹⡇⠰⠀⠀⠎⢴⣶⣆⣀⠀⡀⢀⣤⣰⣿⣿⣿⣿⣿⣿⡿⣳⣿⢳⣿⣿⣿⣿⡿⣼⡟⣾⣿⣿⣿⣿⣿⣿⣿⣯⢠⡄⢚⢹⣿⣶⠀⠀⠀⣍⡐⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠠⠾⣷⣿⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣶⣿⣿⣧⣽⣿⣿⣷⣿⣷⣮⢊⣿⠵⢆⡈⢹⢿⣿⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣛⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣗⠁⣼⡿⢻⣿⣾⣿⣿⣿⣿⣿⣿⡿⣳⢿⣾⣿⣿⣿⣿⡿⢸⣿⣿⣸⣿⢸⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡁⠀⠀⢻⢀⠈⣀⣨⣶⣤⣿⣿⣽⠛⣡⣿⣿⣿⢿⡿⢻⣿⣿⡟⣳⣿⡟⣼⣿⣿⣻⣟⡇⡿⢘⣿⣿⡯⣿⣾⢿⣿⣾⡋⣼⣷⣿⡟⢿⢿⠟⡲⠛⠁⠁⠢⠆⡄⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢀⢦⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣶⠟⣣⣾⣿⣿⣿⣽⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣷⢷⣾⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣦⠻⣿⣧⣿⣿⢹⢼⣼⣿⣿⣿⣷⡻⣿⣿⣿⣿⣿⣿⡿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢫⣖⠂⠀⠀⠂⢰⣿⠿⣿⣿⡟⢿⣿⠃⣴⣿⢿⣿⢿⡾⢱⣿⣿⢛⣹⣯⡿⣹⣿⣯⣵⣟⣸⣿⢣⣿⣵⡿⢾⠿⢲⣶⣎⠛⠁⠋⠻⠿⠶⠶⠈⠐⠙⠉⢠⣠⠀⠀⢀⠄⣀⡊⠴⠖⢠⡀⠈⠀⠀⠁⣤⡤⠴⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⠁⣧⣍⠹⣿⣿⣿⡟⣻⣿⣿⣿⣿⣿⣿⣗⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⡫⣷⡿⢿⣿⣛⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣿⣿⣿⣿⣿⣿⣿⡿⣻⣾⣟⣫⣧⣚⣇⡿⠿⣫⣾⣦⢿⣘⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣎⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠙⣇⣥⣦⡀⡣⠀⠀⠀⠉⠀⠀⣠⣾⣝⣿⣾⡟⣺⣵⡶⣯⣿⡞⠋⢸⣷⣿⣧⣿⢯⣿⡿⣵⣿⠏⣿⡷⣸⣶⠸⣻⣆⡀⣄⣠⠀⠀⠀⡶⠍⠀⠁⠁⠀⠁⠀⠀⡨⠸⡁⠀⠐⠀⣤⡍⡢⡀⡀⠘⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣶⡻⢿⣫⣾⣿⣿⣿⣿⣿⣿⣬⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⣾⣟⣭⣿⣿⣿⣿⣿⣿⣿⣿⣷⡻⠿⣶⣆⣾⡽⠿⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣿⠿⠟⣷⣿⣿⢣⣾⣿⣿⣿⣮⣿⡹⣿⣿⣿⣯⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⠁⠀⠀⠀⠀⡸⠛⢿⣷⣆⡀⠀⠀⠀⡤⣖⣿⣿⣿⣅⢿⣿⣿⣰⣾⣿⣿⣿⢇⣾⣿⡟⢍⣡⣿⡋⣀⣿⣏⠿⣽⣯⡿⠱⣼⣿⣎⢡⠙⠛⢇⢦⠶⡤⠄⠀⠀⠀⠀⠀⠀⠀⠓⠀⠈⠂⠀⠀⠉⠀⠇⣀⡪⠻⠀⠈⠀⢀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⡿⢏⣡⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣩⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⢿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢋⣭⣝⣻⣟⣽⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⢣⣿⠷⣫⡾⢿⣾⣟⣥⣛⣿⣿⢿⡽⣿⡘⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠈⠀⠀⠀⠀⠠⠁⠀⠀⠈⣉⢩⣶⣜⢆⢖⣴⣎⢹⣮⣽⢷⣀⢵⣿⣿⣿⣿⠇⢸⣿⠟⠡⡸⣿⣿⡇⡿⣿⣿⣷⠻⠿⠁⢸⣿⢷⣿⢀⣥⣄⠀⢈⠀⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠯⠞⡀⣴⣶⠇⠀⠈⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⡿⡋⣤⢿⣵⣾⣿⣿⢿⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⣿⣿⣿⡿⠛⣿⡥⠿⢟⣴⣿⠇⣿⣧⡿⣎⢿⣽⣷⣿⣷⣿⣿⣾⢿⣿⣧⡹⣿⣿⣿⣿⣿⡿⠏⣵⡀⠀⠀⠀⠀⠀⢀⣠⣤⣶⣶⣾⣿⣿⣾⣯⣿⡷⣿⣿⣿⣏⢿⡇⣮⡻⣮⢿⣿⡿⢯⣤⢸⡇⣴⡾⠇⡿⢿⠀⢵⣇⢿⣿⣿⣿⢈⣹⡟⢸⡟⡄⠀⠀⢹⡟⣧⠤⠄⠀⠀⠀⠀⠀⠀⠁⠀⠠⠖⢡⣴⣤⣿⣿⣷⡄⠀⠀⠀⠀⠛⠀⣶⣬⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠊⣛⢡⣵⣶⣿⣿⣿⣯⣷⣿⣿⣿⣿⣿⣿⣿⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣯⣸⣿⣿⠿⣻⣿⡿⢿⣿⣫⣭⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⠟⢡⣽⣯⣿⢟⡼⠏⢿⣇⢻⣿⣧⣿⡎⣿⣿⢻⣿⢻⡿⣿⣾⢿⣿⣿⢮⣿⣿⣿⠏⠀⠐⠃⡠⠐⠀⢀⢄⣰⢿⣼⣿⡿⣻⣿⡿⢿⡟⢿⣟⠟⣝⣿⣿⣿⣮⠇⣿⣿⣿⣿⣿⣿⣿⢇⣺⣿⡏⣰⡇⠁⣷⣴⣈⢟⡘⣿⣿⣿⣿⠿⢀⡎⢱⡄⠀⠀⠀⠠⠀⠀⠀⠀⠀⣠⣤⣤⣤⣾⡛⠲⣸⣿⣿⣿⣿⣿⣿⣷⡄⣶⡆⡔⠠⠿⣿⣣⣷⣄⠀⠀⠀⠀⠀⠀⠙⠷⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠻⠁⣿⣿⢫⣝⢿⣾⣿⢿⣿⡿⠿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⠤⢿⡟⠋⣵⣟⡴⣡⣬⣿⡼⣿⣿⠙⠇⠿⣿⣷⡻⣿⣿⢸⣿⣿⣿⣿⡇⡿⠟⠁⠀⠀⠀⠀⠀⣠⣴⣿⣿⢿⣾⣿⢿⣿⣿⣿⣿⠼⣇⢘⡿⢧⣷⢯⡻⣿⣥⢀⣿⣿⣿⣿⣿⣿⣿⢸⣿⡟⠱⣿⡏⠘⡟⠴⡿⣴⣿⣽⣿⣿⣿⢧⡘⢣⢹⠃⢀⠀⠀⠀⠀⠀⠀⢴⣷⣿⣿⣿⣿⣿⠀⠀⣸⢿⣿⣿⢟⣫⡟⢿⣥⡞⢻⠿⢻⣤⡹⣿⣿⣿⣷⡄⠀⠀⢀⡀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣍⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣉⣛⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣽⡗⣿⣯⡿⣹⣿⣾⡿⢻⣻⣽⢟⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣿⣿⢿⢂⣵⣿⡟⣜⣽⣿⡿⣧⡳⢿⣿⣶⣾⣷⢹⣾⣿⡎⣿⡏⣿⣿⣷⡽⠋⠀⠃⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣾⣿⢻⣾⢻⣿⣿⣿⣧⢻⣆⠹⣿⣿⣧⠓⡻⣿⡴⡙⣿⣿⣿⡿⣛⠻⢸⡏⠃⣠⡟⣵⠏⣤⣿⣷⣿⣿⣿⣿⢱⣿⢸⣣⡾⢛⡛⣋⣀⠀⠀⠀⠜⢀⣯⣿⣿⣿⣿⣿⣿⡆⢨⣿⠭⣭⡇⠉⢩⡆⢝⢫⣐⡛⣛⣋⠈⣄⠈⠟⢛⡿⠿⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⢿⣿⣷⡿⣵⣬⣾⣿⣿⣿⣿⣿⣺⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣤⣀⣤⡽⣹⣿⣿⣂⣾⣿⣿⣿⣟⢿⣮⣿⣿⡇⢿⡄⣿⣿⣧⢿⢏⢻⡿⠋⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⡿⣿⣿⢃⣿⣿⣿⣿⣿⣷⡝⠧⣿⣏⠏⣿⢺⣿⣿⣅⢻⣿⣟⣵⣿⠟⠛⢗⣿⣿⡿⣣⣾⣿⣿⣿⣿⣿⣿⢟⣿⡇⠘⣵⣶⣿⣿⣿⣿⣷⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣓⡁⠀⣨⠍⠁⠁⠀⣠⣤⣼⣷⣿⣦⠀⡙⣦⣤⡈⠛⠻⣿⣦⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⡻⡿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣬⡿⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣫⣾⣿⣿⣿⢀⢳⢹⡏⣥⣹⣿⣿⣿⣿⣿⣯⢿⣿⣿⣷⣒⣾⡘⣻⣿⣿⣾⠇⠀⠀⠂⠀⠂⡀⠀⢀⣠⣿⣿⣿⣿⣿⣿⣿⣴⣾⢡⣼⣿⣿⣿⣿⣿⣿⣿⣷⣎⡿⣦⣻⣇⠻⣷⣛⢷⣹⣿⣿⢩⣀⢾⡟⢟⣫⣴⣿⣿⣿⣿⣿⣿⠫⠄⣋⣥⣾⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣭⣻⣿⣿⣿⣫⠄⣀⣁⣂⣤⣤⣴⡾⣟⠿⠛⠋⣙⢻⡝⠈⣞⣿⣷⣄⡸⣿⡆⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⣇⢻⣿⣧⣳⣛⣿⣿⣘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⢻⣧⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣛⣛⣵⡿⣾⢸⣧⣇⣿⣿⣿⣿⣿⣿⣿⣿⡿⣯⣶⢻⣿⣿⣜⢻⡿⠋⢂⠈⠄⠀⡄⠄⠑⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⠙⢳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣮⣃⡻⣀⡻⣿⣷⡜⣿⡟⣾⢩⣖⢳⣟⣿⣿⣻⣿⣿⡿⣛⣡⣤⣾⣿⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣟⡻⣿⣟⣿⣿⣶⣴⣿⣿⣕⣬⣄⢸⡾⠟⠛⢋⣷⡆⠀⣿⣧⡘⠇⣿⣦⣿⠀⠹⡿⡘⣿⣿⡼⣷⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡿⣯⣻⣿⣇⣽⣿⠻⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣀⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣫⢠⣿⣿⢻⣮⢻⣯⢱⣯⣿⣿⡿⢏⣵⣿⣿⣎⣹⣷⣿⠋⠀⠀⠈⢳⡆⠀⠀⠀⠀⣸⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣧⠈⢰⣷⣿⣿⣷⣶⣯⣷⡎⠟⣡⣾⣿⣯⣽⣶⣿⡿⢿⣿⢟⠙⣿⣿⣿⣿⣽⣿⡛⢻⣿⡿⣿⣿⣿⣿⠺⡟⢋⣴⣿⠁⣶⡹⣮⣟⡋⠀⠉⣿⣿⡆⢹⡟⠻⣶⣶⠁⡺⣿⣿⣿⣾⡄⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣜⣷⡿⣿⣟⣿⢠⣝⢿⣿⣿⣿⣿⣾⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣿⣷⣶⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣰⢏⣿⣿⣿⣿⢙⣿⢻⣿⣿⡅⠉⣶⣾⡿⢷⢿⣿⣷⡟⠉⠀⠀⠀⠀⠀⠰⣀⡌⠑⢰⣿⣷⣿⣿⣿⣿⣿⣿⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣼⣿⣿⣿⣿⡿⠿⠟⢣⢴⣿⣿⣿⣿⣿⣿⠛⣿⣌⡛⠚⠞⢿⡏⢹⣿⢟⠃⠁⠀⣿⠀⡿⣿⡻⣿⣄⣶⣟⣿⣿⣦⣹⣧⠘⣿⣿⠀⡇⡘⣿⣧⠈⠀⠀⣿⢟⣶⣿⣹⣟⣹⢿⠇⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣶⣿⣿⣌⢿⣶⣝⣿⣿⣿⣿⣿⡼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡻⣷⣽⣿⣿⣿⣿⣟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣩⣿⣿⣿⣿⣟⠘⠃⢀⣄⠈⣷⣮⣿⡿⠿⠞⠛⡛⠛⠁⠀⠀⠀⠀⠀⢀⣴⡟⣱⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣋⣭⣄⢰⣾⣿⡟⣿⡻⣿⣉⣨⣛⣲⠮⠉⢩⡝⠲⠆⠙⢛⣹⡷⠀⠀⠀⢿⢀⡷⣿⣿⡷⠟⠓⠀⠀⢷⣶⣶⣭⣃⠸⣿⡇⣤⣷⡹⠇⣰⢏⣰⣿⣿⣿⣿⠙⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣿⣿⣿⣿⣏⣾⣿⣎⣿⣿⣞⢿⣿⣿⣿⣷⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣾⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣩⣿⣿⣿⣿⣿⣧⣺⣿⢺⢿⣬⣼⡿⡟⡀⠀⣐⡛⠀⣶⡆⠀⠀⠀⢀⣰⣿⣿⢁⢉⣸⡞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣥⣶⢿⣿⣿⣿⣷⡿⣯⡑⣺⠉⠈⠀⣉⣩⣷⡖⡴⣰⣶⠶⣶⣧⢙⡻⣿⠇⠀⠀⠀⣾⡇⣶⣖⣶⢡⣿⠰⣷⡀⡙⢿⣟⣿⣾⠪⣁⡘⣿⣇⡖⢂⣶⢎⣿⣿⠿⠿⡸⣟⢸⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣝⣿⣿⡿⣿⣷⣿⣿⣽⣿⣿⣶⣍⣻⢿⣿⣮⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣻⡿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣧⡅⡄⠀⣿⡇⠀⣬⣑⠀⠀⠰⢿⣿⣿⡟⢀⣼⣏⢿⣺⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣫⣾⣿⣿⣽⣿⣿⣿⢿⡯⣻⣮⡉⢉⣿⢇⣀⡿⢫⣿⢠⣹⣿⣹⢇⣿⢏⣾⡷⠃⠀⠀⠀⠀⣿⡁⣿⣿⣿⠘⣿⡧⢿⣯⣰⣼⢿⡿⠻⣶⡘⣁⡻⡿⢵⣶⢻⣿⣿⣿⣿⢉⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢿⣟⢗⡆⠀⢻⣷⠀⠹⣿⣄⠀⠀⠤⠀⠁⠁⠿⠿⠿⠏⢷⡿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣥⣿⣿⣿⣿⣿⣿⣿⣿⣵⣿⣿⡻⠿⡋⣿⣟⣾⡿⣁⡿⠟⠿⠿⠛⠋⠈⠁⠈⠋⠀⠀⠀⠀⠀⠀⣿⣷⢻⣿⣿⣷⡹⣿⣼⣿⣿⣿⣿⣿⣿⢆⣡⡿⣇⣲⣷⣴⡄⠉⠉⣽⡇⢊⢨⣿⣟⣻⣿⢸⣦⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣭⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡻⠷⡆⠀⣾⡇⣧⡀⠘⢿⣿⣿⣿⣿⣶⣶⣶⣾⣿⣿⣿⣿⣭⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣥⣿⣿⣿⣿⣿⠿⣿⣿⢟⠽⣿⣹⡿⣣⣾⣇⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⡀⠀⠀⠀⠀⠀⠀⢻⡏⣾⣿⣿⣿⣽⣘⣻⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡫⣋⢿⢿⣿⣦⣻⣄⠸⣿⣿⡯⢬⡯⣼⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣧⡹⣿⣿⣿⣿⣯⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣿⣀⠸⡟⣿⣿⡆⣌⣙⠺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣝⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣯⣿⣿⣿⣿⠟⣥⣿⣿⣿⣽⣿⣿⣿⣼⢿⣯⣼⣿⡿⣣⣶⣿⣿⣿⠟⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠰⣾⡇⠛⣿⠝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣥⣾⠏⢮⣿⠯⢿⣿⣿⣦⣿⣽⣿⣶⡳⣿⣿⣿⣿⣷⣤⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣧⡹⣿⡿⣿⣿⣷⣌⢿⣿⣿⣿⣯⢿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢛⣿⡇⣮⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣾⢻⣿⣿⣿⣿⣿⡿⢟⣥⣿⡿⣯⣟⠿⣧⣹⣿⣽⣿⠿⢛⣻⣽⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢠⡙⣷⣴⣿⣿⢹⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⡇⠊⣯⣓⣮⣽⣟⢿⣿⡼⢿⣿⣷⢻⣯⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣧⣹⣧⣻⣿⣿⣿⡌⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⢿⣿⣿⣽⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣯⣶⢸⣿⡘⣿⡟⣿⡸⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⢡⣾⣿⣿⣿⢟⣽⣿⣿⣿⣿⣿⣿⠟⣛⣭⣭⣭⣶⣾⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣅⠙⣿⣿⢿⣿⣿⣿⣻⣾⣿⣿⣿⣿⣿⣿⣿⣷⣿⢟⡜⠘⢊⣿⣿⣿⣿⡷⣿⣝⡛⠛⣛⣾⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⣿⡟⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣾⣿⠟⣿⣿⣇⢛⡼⣿⣿⣽⣿⢿⣿⡻⣾⣿⣿⣿⣿⣿⣿⣿⢿⣷⣿⣿⣿⣿⠋⣸⡿⢛⣫⣵⣿⣿⣿⣿⣿⢟⣯⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⣿⡘⣷⣿⣿⠏⡆⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⠟⣫⣵⣻⡙⢫⣿⣿⣿⣿⣿⣿⢸⣿⣾⣽⣶⣆⣹⣿⣿⣿⣯⣻⣿⣿⣿⣆⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⠛⢿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡟⣧⣿⣿⣿⣏⣯⣏⢻⣿⣿⡼⣯⡻⣿⡾⣿⣿⣿⣿⣿⣿⣿⣷⣟⡧⣿⣯⢻⠟⢁⣠⣭⣛⠛⢿⡾⠟⣫⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⢡⣶⢸⣿⠁⣾⣿⣿⣋⣭⣿⣿⣯⣴⡿⣻⣵⣧⠆⠀⣙⢿⣿⣿⣿⢹⣿⣿⣿⣿⣿⣿⣧⣻⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠹⣿⡟⠋⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣷⣿⢿⣿⣿⣿⣿⣿⡮⣿⣿⣯⢾⣷⣎⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡿⢁⣵⣾⡿⢿⣿⣿⣷⣿⠇⣾⣿⣿⣿⣿⣿⡿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠐⠁⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⡟⢋⣥⣼⣿⣿⣦⢻⢻⣿⣿⢿⣟⡛⠋⣀⣴⣿⣿⢃⠒⠇⠀⢠⠙⢿⣿⣿⣿⣶⣾⣿⣿⣿⣿⣷⡿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⣀⣠⡀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣷⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⢊⣧⣠⣹⣿⣿⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢛⣐⣿⣿⣿⡾⢶⣽⣿⣿⡸⣀⣿⣿⣿⣿⣿⣿⠾⡤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣶⣶⣘⣿⣷⣦⣶⣾⣿⣿⣿⣾⡏⡎⠀⡀⠀⠀⠀⠈⢿⣿⡸⣿⢻⣿⣿⣿⡏⢿⣷⡿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠉⠂⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣞⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣏⣷⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠟⢙⠛⣤⠿⠫⠼⢿⣿⣾⣿⣿⣿⣿⣿⣿⡿⠿⠏⢿⣿⠟⣴⣿⣾⣿⣛⢯⣀⠀⢹⣿⣿⣧⣿⣿⣿⣿⣿⣿⠟⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣦⣻⢿⣿⣿⣿⣿⣿⣿⣏⡨⠅⠀⠀⠀⠀⠀⠀⠈⣿⣿⣻⣿⢿⣿⣿⣿⡎⢻⣿⡜⣿⣿⣾⢾⣿⣮⣝⠀⠀⠀⠀⠆⠠⠀⠀⠀⢛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⢿⣿⣿⣿⣿⣿⣿⣿⡽⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣿⣿⣿⣻⣿⣿⡯⣿⣿⣷⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⢂⣴⢃⣰⠿⣴⣿⣟⢿⣿⣿⣿⣿⣿⣿⣿⢡⣶⣿⡿⠿⠟⣾⣿⣿⣶⣶⣾⣿⢏⣤⣿⡿⡛⣹⣿⣿⣿⣿⣿⣏⣾⢇⣦⢸⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠈⣿⣿⣿⣿⣿⣿⣿⢻⣽⣿⣿⡿⠃⠠⠄⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣻⣿⣿⣿⣿⣿⣆⣻⣿⡟⣿⣿⣿⣿⣿⣾⣦⠰⢀⣀⣶⣶⢒⠒⢊⡨⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣾⣿⣿⣿⣿⣿⣻⣿⡿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢡⣾⠟⣿⣿⢘⣿⣷⣿⢸⣿⣿⣿⣿⣿⣿⡿⢸⣿⣟⠟⠓⠂⢹⣿⣿⡿⣿⣫⣷⡿⢸⣿⡿⢳⣿⣿⣿⣿⣿⡿⣼⣿⠾⠧⣾⣿⡻⣿⣿⣯⣼⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⡿⣿⣧⣿⣿⣿⣿⢿⣾⣿⣞⣿⣿⣿⡗⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣾⢿⣿⣿⣿⣿⣿⣿⣷⡿⣿⣿⣜⣿⣿⣿⣧⠁⠀⠀⠀⠀⠀⠩⢩⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⣿⣿⣿⣯⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⠞⢿⣿⣿⣿⣿⣯⣷⣿⣿⣿⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢱⣿⠏⢸⣵⣿⣜⢻⣿⣿⣼⣿⣿⣿⣿⣿⣿⣇⢸⣿⠙⢆⠢⡐⡘⣿⣿⣷⡉⣽⣿⢹⣿⡿⣱⣿⣿⣿⣿⣿⣿⠿⢿⣧⣦⢀⣿⣿⣿⣸⣿⣟⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⢾⣿⣿⣿⣿⣿⠟⠁⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣷⣿⡿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣶⣜⠂⣠⢄⠠⠀⠀⠀⠀⠀⠈⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣻⣿⣯⣝⢿⣟⢿⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣇⢿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⡏⣠⣿⣷⡜⡛⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣼⣿⡄⣬⡳⣿⣦⠻⣿⣿⣤⣉⡱⢿⣯⣿⣿⣿⣿⣿⣿⣿⣽⣆⠏⣯⢹⡆⣿⠿⣿⣿⣿⡆⡋⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠂⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⢀⡀⠀⣀⡀⣿⣿⣿⣟⣛⢿⣿⣧⣿⣿⡟⢟⣁⣚⠆⠓⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣯⡿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠈⠀⠀⠀⡀⣤⣄⡀⠀⣀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⢻⣿⣿⠻⣿⣝⡿⣿⣿⣿⡿⣿⣿⣯⣿⣿⣷⣯⢿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⡯⣷⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣧⡹⣧⢻⣿⣾⣭⣥⣯⣽⣿⠿⣿⣶⣭⣟⡿⢿⣿⣿⣿⣿⣿⣿⣷⣍⣿⠓⢿⣺⣿⡿⢟⣵⠧⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠀⠀⠀⠀⠀⠀⠀⠀⠆⠙⠿⠟⢿⡄⢹⣧⣿⣿⣿⣿⣿⣟⢿⣿⣿⣿⣿⠘⠻⣿⣿⣶⡄⠀⠀⠀⠀⠀⠐⠀⠀⠁⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣯⡿⣿⣿⣿⣿⣍⠿⣿⣿⣿⣿⣿⣿⣦⡀⠀⡀⢀⠑⠌⢿⣿⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡿⢿⣿⣿⣿⣷⣬⣫⣿⣷⣼⣿⣸⣯⣽⣽⡞⢿⣭⣭⣭⡷⣽⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣭⣶⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣯⣬⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣭⣽⣏⣼⣿⣿⣿⣿⣿⣿⣿⣿⣧⣾⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⡟⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⢐⣌⠻⢨⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢏⠶⣦⠈⢿⣿⣿⣧⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⡔⣽⣿⣿⣿⣿⣿⣿⣿⣦⠀⠘⢧⡀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠯⣷⡾⣿⣯⠻⠿⢿⠿⢯⣯⣽⣦⣽⠿⠟⢿⣿⣾⣿⣛⡿⣿⣿⡿⣿⣿⣼⢯⣝⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⠁⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⡏⢸⡷⠀⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢹⣇⣀⣹⢿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣧⡻⣿⣿⠿⢛⣋⣡⣶⣌⣿⣿⣿⣿⣟⠦⠀⠙⠆⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⣿⣷⣝⣯⠳⣭⢿⣿⣿⣿⣿⣿⣿⣿⣷⣧⣿⣮⡟⣿⡯⣿⡿⣿⣟⢿⣿⣿⣿⣯⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⠇⠀⠀⠀⢰⣿⠯⡮⠩⣿⣻⡿⢁⣿⡇⠋⠡⣿⣿⣿⣟⢿⣿⣿⣿⣿⣹⣿⣿⣿⡆⡹⡿⡛⡿⣷⣶⣭⡷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⡿⣿⠇⣵⣾⣿⣿⡿⠟⡙⣽⣿⣿⣿⣿⣿⣿⣦⡀⠀⣠⣾⣞⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡞⣿⡿⣿⣷⣝⢷⣬⣍⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡿⣿⣽⣮⡻⣷⣝⣿⣌⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣽⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣷⣿⣿⣿⠀⠀⠀⢀⣿⣿⡦⢙⣻⣿⣿⡇⢸⣿⡇⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣿⣿⣟⡁⠁⠹⡿⣎⢟⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⡠⠀⠀⠀⠀⠀⠀⠀⠛⢿⣿⣿⢀⡌⢻⡻⢿⡪⠁⢻⣼⣿⣿⣿⣿⣿⣿⣿⣿⡀⢸⣿⣿⣦⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡞⣿⡻⣟⢿⣦⢹⣿⢷⣿⢿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣮⣿⣳⣛⢦⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣻⡿⢫⣿⣿⣿⣿⣿⣟⣿⣿⡿⣫⡿⠀⠀⠀⠀⠀⠀⠀⠀⣀⣄⡴⢰⣿⣿⣿⣿⡏⠀⠀⠀⣼⣾⣿⣾⣿⣿⣷⣆⢄⢸⢻⣷⡀⠀⠦⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡡⠀⠀⣷⣼⡆⡿⣿⣿⣿⣿⣄⣄⡘⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣇⣿⣦⡿⣷⣶⣾⣿⣷⠸⣿⣿⣿⡟⣿⣿⣿⠃⣸⣿⣿⣿⣿⢙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⢿⣌⢷⣿⣷⡽⣿⡻⣿⣦⣜⢷⣿⣿⡿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣟⢷⣿⣶⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⣵⣿⣟⣥⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⠁⠀⠀⠀⠀⠀⠀⠀⠠⠛⠀⠀⣸⣿⣟⣿⣿⡇⠀⠀⠀⣿⣿⣷⣈⣹⣾⣿⢸⡏⠘⠿⣿⣷⡁⣠⠀⣿⣿⣿⣿⣿⣿⡿⠛⠉⣐⣋⣤⣶⣿⣿⣤⡏⣿⣿⣿⣿⢿⣿⡜⣷⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡿⣞⣿⣿⣿⣿⣿⣿⣿⣗⣜⠻⢿⣿⢿⣟⣷⣿⣿⣿⣛⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⣮⡻⣾⣻⣿⣜⢷⣸⣿⣿⣿⣿⣿⣷⣟⣯⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣫⣿⢿⣾⢣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⡁⠞⢧⣠⡠⠀⠀⠀⢰⣿⣟⡟⣿⣿⡇⠀⠀⢠⣿⣿⣿⣿⢻⣿⢗⣿⣷⣔⢠⣿⣿⡇⣉⠀⢀⠊⢻⣛⣫⡁⠀⢀⣼⣿⣿⣿⣿⣿⣟⢿⣷⣿⣿⢻⣿⣯⣿⣷⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣽⢿⣿⣿⣟⢿⣿⣿⣿⣷⣞⣻⣷⣽⣿⣍⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣙⠛⣿⣟⢿⣆⣽⣻⣿⣿⣿⣿⣿⣿⣿⣮⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣾⣿⣿⣾⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣿⣿⡿⠀⠈⠀⢀⡀⠀⠐⠁⠀⠀⠀⣾⣿⡿⢳⣿⡟⠀⡤⠀⠈⢿⢼⣿⣿⣾⣿⢸⣿⣿⣿⣿⣿⡿⣷⣦⣿⣿⠀⠿⢋⣿⣶⣶⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣟⣿⠘⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣷⢻⣿⣿⣦⠠⣶⣟⣉⢛⢳⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣿⣐⣝⢿⣲⣻⣞⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣿⣿⣿⡿⣿⣼⣿⣿⢻⣱⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⢿⣟⣶⠐⠀⠀⢸⡛⢸⣿⣿⣿⣿⣎⢿⣿⣿⠟⣵⣶⣿⣿⣿⣿⣦⠢⣿⣿⣷⣶⣶⣯⣝⠿⣿⣿⣿⣿⣯⡏⡻⣿⡿⢿⣽⣿⣮⡈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡝⣿⣛⣵⣽⢿⣍⠠⣝⢛⣛⣛⣉⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⢮⣳⢳⣝⣳⡝⢏⣻⣿⣿⣿⣿⣿⡷⣿⣿⣿⣷⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⢋⣶⣿⣿⣿⣿⣾⣿⣿⢟⣵⣿⣿⣿⣿⢇⣿⣿⣿⣿⣿⣏⡿⣿⣿⣿⢸⣿⠀⠀⠒⠂⠀⠀⠀⠀⠀⠀⣾⣿⣏⣵⣿⣟⡏⠀⠀⢠⠋⣰⣿⣿⣿⣿⣿⣾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡙⣷⢹⣯⣽⣻⣿⣛⣛⣿⠿⠿⣿⣿⣿⣿⡾⣿⣷⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠠⡀⠀⠀⠀⠀⠀⣰⣿⣿⣷⢻⣟⢾⡽⣷⣝⠿⢞⠷⠾⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣻⣦⣜⠿⣿⣾⣳⣮⡻⢿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣶⡟⣸⣿⣿⣿⣿⣿⣿⡿⣫⣾⣿⢻⣸⡿⣡⣿⣿⣿⣿⣿⣯⡿⣵⣿⣿⡟⣬⣭⡄⡷⠁⠀⠀⠀⠀⠀⠀⢸⡿⠿⣿⣿⣯⣿⣧⠠⢠⠌⣰⣿⣿⣿⣿⡿⣿⡟⢰⣾⢿⣿⣿⣿⣿⣿⡿⣱⣷⣿⣷⣿⣿⣿⣿⣿⡿⠉⠀⠀⠀⢿⣿⣷⣇⢾⣿⣿⣻⣿⣿⣿⣿⣿⣦⢻⠄⠀⠃⠀⠀⠀⢀⣴⣿⣿⣿⣿⠈⣷⢸⣧⡈⢿⣭⣭⡀⣾⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⡼⣿⣧⣼⣭⣯⡻⢿⣧⡉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⣠⣿⣿⣿⣿⣿⣿⣿⣳⣿⣿⢏⣾⡟⣼⣿⣿⣿⣿⣿⣿⡿⣳⡟⣿⡿⡼⣿⠿⡦⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⡿⢿⡟⠀⣾⢰⣿⣿⣿⣿⣿⣿⡟⢀⣽⣿⣿⣿⣿⣿⣿⡿⣵⣿⣿⢹⡏⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⣸⣇⣿⢿⡆⣿⣿⣷⣯⣾⣿⣿⣿⣿⣷⡱⠆⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⢿⡾⢯⣭⢭⡥⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⢸⣿⣿⡌⡿⣿⣿⣿⣿⢾⣩⡿⣧⣽⢿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣭⣾⣿⣾⣿⣿⣿⣿⣿⣿⣿⣅⡿⣵⠟⢡⢏⡿⣿⣿⠀⠉⠁⠀⠀⠀⠀⠰⠶⠶⣶⣶⡀⢹⠏⣀⠘⢁⣾⣿⣿⣿⣿⣿⠟⣰⣿⣿⣿⣿⣿⣿⣿⣿⣁⡿⣏⠿⡆⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠠⣯⣽⡟⡎⣇⣾⣿⣿⣿⡿⣿⣿⣿⣿⣿⣷⡀⠆⢀⣴⡿⣿⣿⣿⣿⣿⣿⡆⣿⠹⣿⠇⣿⣯⠹⢱⡖⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⠰⢶⣾⣇⣴⣿⣮⣿⣿⣿⣮⡿⣿⣯⣽⣷⣙⢿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣼⣿⣿⣿⣿⣿⡿⣹⣿⢿⣿⣿⣿⣧⣿⣢⣿⡿⣥⣿⣿⡷⠐⠒⠒⠚⠓⢰⣿⣿⣿⣿⣿⣅⠈⠀⠁⣴⣿⣿⣿⣿⣿⣿⡏⣰⣿⣿⣿⣿⣿⣿⣿⣿⠇⣿⣧⠿⠷⠉⠀⠀⠀⠀⠀⠀⠀⠀⡠⠆⣼⣿⣿⡇⠰⣿⣄⢻⣿⣿⣿⡻⣿⣿⣿⣿⣿⣿⣦⣼⣟⣿⡝⣿⣿⣿⣿⣿⣯⣼⣄⣿⠀⡿⠿⠂⣨⢾⣿⣿⣿⣿⡿⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣷⣻⣿⣹⣿⣿⡟⣿⣿⣟⢿⣿⣮⡻⣯⣿⣿⣯⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡖⣿⣿⣿⣿⣿⣿⣿⢻⣿⡿⣽⣿⣯⣿⢇⣞⣿⣿⣿⣿⣿⣾⠀⠀⠀⠀⢠⣾⡿⣿⣛⣻⠯⠻⢧⣤⣾⣿⣿⣿⣿⣿⣿⡿⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⢇⣾⣿⣿⡏⠸⣦⠻⣿⣶⡛⣿⣿⢿⣿⣮⣻⣿⣿⣿⣿⡇⢹⣇⢿⣯⣝⣿⣿⣿⣿⣿⣿⡨⣼⣿⢿⣏⣿⣿⣻⣿⣿⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣽⣿⣏⢰⣿⣿⣿⣍⢻⡿⣿⡏⢿⣿⣿⣿⣿⣿⣿⣷⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⢙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣴⣿⣿⣿⣿⣿⣿⣧⡾⣷⢧⣿⣿⡿⢣⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠈⣿⣿⣬⣭⣄⡀⡀⣼⣿⣿⣿⣿⣿⣿⣿⠸⢁⣾⣿⣿⣿⣿⡿⣿⣿⣿⠇⠀⠀⠀⠠⠀⠀⠀⠀⢀⣄⣸⣿⡿⣧⣼⣿⣿⡿⠃⡶⣮⣤⡹⣿⢿⠐⢩⣟⣻⣿⡟⠿⣻⣿⢿⣿⡨⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⢻⢻⣾⢋⣿⣿⡏⣿⣿⢇⣿⡿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣭⣾⣿⣿⠻⣿⣿⢣⣾⣿⣿⣿⣿⣿⢻⣿⣷⣿⣯⣟⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢳⣿⣿⣿⣿⣿⣿⣿⣿⢿⢯⣾⡿⣿⢇⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡿⣣⡟⣿⣿⣿⣿⣿⣿⢟⠀⢸⣿⣿⣿⣿⣿⣷⣿⣿⡏⠀⠀⠀⠀⠀⣀⣄⣴⣦⣿⡿⡟⣿⣾⣿⣿⣿⡿⢣⣦⣝⢻⡿⣿⡿⡆⠀⢀⣭⣿⣟⣷⣿⣿⣿⣿⣿⡇⢹⣟⣧⣿⡽⣿⣿⣿⣿⣟⣿⠈⣿⣟⣼⣿⣿⡇⣿⢿⣾⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⢻⣿⣿⣿⣿⣿⣿⣯⣻⣿⣿⣞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣼⣿⣿⣯⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⣿⣯⣏⣿⣿⣿⣿⣿⡜⡀⢿⣿⣿⣿⣿⣯⣿⣿⡏⣀⣠⣤⣶⣾⢸⣿⢹⣿⡿⠛⣱⣿⣿⣿⣿⣟⡟⡅⣾⣿⣿⣈⢳⣻⣿⡄⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣯⣿⣧⡿⣷⡙⣿⣬⣿⣧⢻⣷⣿⣿⣿⡇⢋⣾⣿⣿⡗⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣼⣿⣿⣿⣿⣻⣿⣿⣷⡿⣿⣟⣷⣿⡿⣯⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⡝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⡇⣿⣿⣝⣿⣿⠟⣿⣿⢠⣿⢺⣿⣿⣿⣿⣽⣿⣯⡈⣿⣿⣿⣿⡏⣶⠸⠞⣋⣲⣿⣿⣿⣿⣿⡧⢫⣶⣧⢻⣿⡿⣿⣧⢷⡛⣧⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣾⣿⡟⣿⣿⣧⠻⣿⣿⢿⣿⣿⡼⣿⣿⣿⡿⣥⣿⣧⢹⡟⣿⣯⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣟⢷⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠉⠉⠉⠉⠉⠉⠉⠉⠙⠛⠛⠛⠛⠛⠉⠉⠉⠙⠛⠉⠉⠉⠉⠁⠉⠁⠉⠉⠉⠉⠉⠉⠉⠛⠛⠁⠙⠙⠉⠛⠛⠛⠛⠛⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⡿⣾⣿⢋⣿⣿⢸⣿⣿⢸⣿⣿⣿⣿⣽⣿⠿⣟⣛⣥⣥⣶⣿⣿⣿⣿⣿⣿⡿⣋⣴⣿⣿⣿⣧⢸⣷⣻⣿⡞⣿⢸⢢⣿⣿⣿⣿⣿⣮⣹⣿⠋⠁⣼⣿⣿⡷⣿⣿⡟⣧⢹⣿⣷⣬⣻⣿⢸⣿⣿⣿⢨⣿⣶⣶⡧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣙⢿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⣿⡷⣿⣿⢇⣿⣿⠈⠙⠛⠸⣿⣏⣿⣿⣳⣿⣿⡷⣶⣛⣿⣟⣛⣻⣿⣟⣿⣿⡿⡟⣠⣾⣿⣿⡿⣿⣿⣿⡹⡧⣧⡻⣾⡹⡎⣻⣿⣿⣿⣶⣽⣽⡿⠃⠀⠐⣇⢸⡟⣿⠘⣏⣿⣟⠈⣿⣾⣟⣿⢰⣜⢿⣿⢯⣾⣻⣧⣿⡅⣿⣟⣿⡗⣿⣣⣿⣿⣿⣿⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣷⡿⣿⣧⣿⠋⣿⡎⠟⠉⠁⠀⠃⠛⠛⠛⠟⠿⠽⢿⣿⣇⢷⣽⣷⡹⣿⢰⣿⣿⣿⣌⣿⣿⡟⠁⠀⠐⡀⣿⣏⣿⡽⣇⣷⠻⣿⣀⣿⣿⢿⣻⣮⢋⡸⣿⣼⡇⢯⣾⣿⡇⣿⡿⣯⣾⣿⣿⣿⣿⣿⣽⣿⣿⢿⣿⢿⣻⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠄⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣧⣿⠁⠀⠀⠀⠀⠀⠀⠙⢿⣿⣧⣿⣿⣿⣿⣿⠶⠟⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠻⠊⢿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠂⢸⣿⣿⡷⢻⣿⡀⠿⣿⢹⣿⣼⠋⣣⣿⣷⢹⣿⣷⣾⣿⣿⣇⣿⡆⣿⣯⢻⣿⣿⣿⣿⣟⣿⣿⣿⣹⣾⣿⣿⢻⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢦⡀⠀⠀⠀⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡿⠻⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⢿⣧⣿⣷⣷⡿⣌⣿⣎⢻⣾⠒⣿⣽⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⠷⠿⠿⠿⠿⠿⠿⠟⠿⠟⠓⠛⠛⠛⠛⠉⠉⠉⠁⠀⠀⠉⠉⠉⠉⠉⠉⠀⠉⠉⠙⠛⠻⠿⠾⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣾⡿⠷⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣉⣭⡭⣽⣶⡀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠛⠙⠻⠿⣼⣿⣧⣹⣷⢿⡜⣿⣿⣿⣿⠿⠿⠿⠿⠛⠛⠉⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣿⣶⣷⣿⣿⢷⣦⣄⣄⣀⡀⠀⠀⠀⠀⠈⠉⠙⠻⠿⢿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣷⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣻⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠘⠃⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣤⣀⣠⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣄⣀⣀⠀⠀⠀⠀⠉⠙⠛
⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⣤⢤⢴⢤⣄⣀⠉⠙⠻⣶⣆⡐⠀⠀⠀⠤⠤⠄⠀⠀⠂⠐⠂⢰⣿⣿⣿⣿⡈⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠐⠀⠀⠠⠤⠦⠤⠤⣠⣤⣀⣤⣤⠤⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣌⢻⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣴⣦⠀
⡙⠛⠪⠁⢠⢀⠀⢀⡀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠂⠤⣌⣁⠈⠄⠀⠀⠀⠀⠀⠑⠈⠀⣀⢀⣀⠀⠀⠀⠀⠀⠙⠛⠛⠛⠛⠛⠛⠋⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠼⠂⠀⠀⠀⠀⠀⠀⠀⠀⡶⠒⡒⠰⡖⣂⣉⣭⣉⢷⣶⣶⠇⠀⠒⠀⠀⠀⠀⠹⣿⣿⣧⠻⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠶⢶⣶⣖⠒⡒⢲⣒⠒⡂⢶⣒⣶⣤⣤⢠⣤⣤⡤⠠⠃⢃⠀⠀⠀⠀⡀⠄⠀⠀⠀⠀⠀⠀⠀⢀⣐⣀⠀⠀⠀⠀⠀⠀⠀⠈⠈⠒⠦⣤⣄⣀⠀⠀⠀⠀⠈⠀⠂⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠈⠙⠛⠞⠲⣄⣠⣀⠀⠀⢀⠀⠀⠀⠀⠘⠻⣿⣷⣹⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⣠⣶⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⢿⠿⢿⡿⠿⠿⠿⣻⣳⣶⣿⣾⣈⠃⠼⠩⠁⠉⣿⠻⠿⢛⣛⣬⣭⣵⣶⣽⣛⣷⣶⣖⠙⢛⡛⠿⠟⢿⣏⣭⡉⠀⣤⡀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠉⠒⠶⠤⣤⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠋⠁⠛⠝⠛⠁⠀⠀⡀⠀⠈⠉⠋⠛⠛⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠬⣤⡀⠀⠀⠀⠐⢴⣂⠘⠉⠉⣹⡿⢿⣛⠻⠿⠿⠻⢿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡟⢿⠿⠿⢿⣿⣿⠿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⡭⢞⣻⣺⣷⢷⣠⣶⡶⢦⡄⢠⠴⢶⠆⣀⣤⡄⣤⢉⡅⣭⢁⣤⣛⢒⣐⡓⣂⣚⠛⠛⠻⠿⠶⠾⠶⢶⣿⢾⣿⣴⣦⣤⣤⣤⣤⣤⣤⣄⣀⣰⣦⣭⣙⣭⣆⣈⡁⣘⣉⣀⡀⢀⣀⣀⣀⣀⣀⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⡀⠉⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠈⠉⠁⠀⠀⠘⠀⢠⣶⣤⣤⣬⡭⣩⣭⣤⣤⣄⣤⣤⣤⣠⣤⣤⣴⣶⣶⠶⣶⣦⣓⡖⠞⠒⠒⣿⣿⣧⣾⣞⡥⢿⣁⣀⠀⢉⣉⣋⣉⣁⣤⣤⣤⣤⣴⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣴⡾⡛⣌⣛⣻⣶⣦⣤⣼⣯⣒⡶⢻⡟⣡⣀⣠⡿⣤⣀⡶⣛⡟⣢⣶⣶⣻⣷⠶⣸⣔⣛⡷⣂⠽⠰⣆⣦⠀⢠⡔⠲⢠⣄⠠⢩⣭⣍⣛⠛⠻⠛⠳⠟⠹⢭⡵⠞⣟⣿⣻⣻⣿⣟⡟⢡⣶⣶⣶⢨⣤⡄⢨⡉⢀⣀⣀⣀⠀⡀⠀⠀⠀⠒⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡄⠀⠸⠀⠀⠠⣦⣦⢤⡼⠃⠀⣤⢀⠀⠚⠦⣂⢲⣦⣴⣶⣶⣦⣽⡿⠛⠿⠿⠯⠨⡿⠯⣝⡿⢙⣧⣽⣿⣟⣯⣿⣿⢛⡿⣿⣿⣿⣲⣏⣤⣤⣧⣦⣴⣯⡿⠽⠻⢏⡉⡙⠁⢴⣅⣙⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣷⣿⣿⣿⣿⣷⣻⣿⣿⣿⡿⣩⣿⣿⣿⣿⣛⡛⢡⣿⣻⢽⢿⣛⣸⣛⣯⣟⡛⣠⣴⣟⣴⢶⡨⣼⡖⢛⣋⣛⣓⣽⣿⡶⣯⣛⡛⢻⠿⣻⡧⣾⣿⣷⣿⣧⣻⣟⠿⣿⣿⣶⣆⣶⢂⣨⣭⣭⠉⢚⣉⣑⣚⡳⡶⢾⣿⣿⡿⣷⣾⣿⣿⣿⣶⣷⣚⠿⣿⣿⣿⣶⣶⣶⣤⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡓⠠⠀⠀⠀⠬⢯⠤⠀⠀⠀⠉⣿⣿⣿⣂⠨⣿⣿⡿⢿⠿⠋⢀⣀⣤⢄⣀⣄⣴⣶⣦⡴⣿⣿⣯⣟⡳⢀⠺⣷⣾⣿⣿⣯⣹⢿⢿⣿⣿⣛⠉⠁⠀⠬⢽⠉⠙⠃⠠⠤⢑⡛⠩⣌⡉⠉⠛⢛⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣵⣾⠿⣿⣿⣿⡿⣿⣯⣰⣿⠷⣵⣞⣒⣻⣿⣽⢕⡷⠶⣿⣋⡩⣀⣁⢀⣶⣟⣿⣿⣿⠿⠷⠟⣒⣋⡀⢙⡛⣛⢗⣛⣧⡷⢶⣿⣍⣡⣽⡾⣏⣭⣟⣴⣿⣶⣛⣿⣛⣩⣿⠗⡢⠿⠾⠷⢶⢞⣿⢟⣣⣶⣶⣺⣿⡿⣿⣿⣟⣛⣒⣘⣛⢛⣛⣛⣛⣛⣛⣙⣛⣉⣉⣒⣀⢀⣀⣀⣀⡀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⣤⡀⠠⠀⣄⠀⠀⠀⠀⠸⠟⠿⢁⣠⣤⠆⠨⠍⣀⠴⣰⡶⠶⠿⠿⠿⠿⠿⢥⣌⣿⣿⣿⣶⣶⣶⣶⣿⣈⠑⠐⠿⠭⠽⠿⢖⣶⣶⣾⣭⣤⣤⣤⣲⣾⣶⡿⢉⠓⠒⠀⠤⢄⠀⢒⠒⠈⠹⠿⠿⠾⠿⠯
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⢼⣻⠟⢻⣬⡿⣟⢄⣹⣿⢻⣳⣾⣇⣤⡿⠿⣂⡷⠄⣤⣤⡿⣭⠊⠘⣻⣿⣿⣿⣿⣿⣿⣻⣷⣾⣿⣿⡿⣷⣾⣆⠟⠁⣠⣶⣆⠩⣙⣿⣿⣿⢿⣷⣿⠟⡿⣿⣿⣿⣻⢿⣷⣶⣶⡗⢲⠿⢶⢾⣟⣼⣟⣾⣿⣻⡟⢡⣾⣿⣿⡛⣻⣒⣾⡿⡿⢿⢿⠿⢾⣿⣿⣿⣾⣿⣟⣻⣿⣿⣩⣿⣷⣻⢿⣹⣶⣦⣶⣶⣦⣴⣶⣦⣤⣄⡀⢀⣀⣀⡤⢤⣤⣤⣄⣀⣀⣀⣀⣀⠹⣷⡄⠀⠀⠀⠀⠻⢿⣦⠀⡉⠁⠄⠀⢀⣀⡂⣻⡿⢫⡷⠿⠛⠶⠛⢓⣱⠿⠲⠢⠤⢴⣀⠘⣹⠛⣯⣭⣙⣿⣛⣛⣒⣚⣈⠥⣭⣛⣷⣶⣶⣬⣉⣘⣉⣙⡛⠷⠦⠬⡯⣝⢫⠶⠾⠀⠠⣀⠤⣄⡀⠂⣦⣬⣠⣍⣛⠷⠶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣷⣽⣛⣿⣿⢿⣾⣿⣾⣿⣶⢖⣶⢟⣷⡿⣶⠤⣯⣶⣿⠖⢠⣲⣴⢦⣾⣿⣿⣿⣿⣿⠿⢿⣿⣿⣷⣾⣽⣶⣿⣿⣗⠉⣬⢻⣿⣿⡾⣿⣿⣟⣟⣻⣿⣏⣷⣿⣶⣿⡿⢿⣨⣿⣾⣾⡷⣾⣿⣲⣾⣿⣧⣴⣿⣷⡾⠿⣟⣿⣿⣷⣾⢿⠿⡿⢿⡿⠾⢇⣲⣖⣴⣶⣿⣛⣻⡽⣯⣿⣛⣏⣽⣟⣿⠾⣻⣜⡿⣿⡿⠿⠶⢫⣿⣿⣿⣷⣾⣶⣶⣿⣾⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣾⣶⣶⣶⣶⣶⣴⢤⣥⣯⣦⣤⣵⣤⣭⣤⣦⣼⣿⣯⣬⣁⣠⣤⣷⣶⣲⢤⣀⣰⠕⢓⣺⣶⣤⣦⣯⣤⣤⣽⡿⢽⣾⣽⣛⣟⣶⣲⣦⠟⢭⣧⢻⢟⣿⣛⡶⢶⣷⠦⠴⣉⠉⣶⠀⠠⣄⣉⠤⠲⠉⠅⣀⡠⢉⣉⠈''', 0.0005)
def shop_art():
    echo('''⢀⠀⠀⠀⡐⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⡿⠿⢟⣛⣬⡵⣿⣻⣿⠉⣿⣿⣿⣿⣾⡇⠀⠀⠀⠀⣼⡇⣿⣿⠏⣃⠀⢹⣿⣧⣰⣿⣿⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⠉⣿⢿⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⣿⣿⠇⠶⠀⠀⢀⣴⣾⣐⣿⢻⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡏⡁⠀⢀⢸⠁⠀⢻⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⡿⢿⣿⣿⣷⡻⣿⣿⣿⣿⣿⣿⣿⠞⡟⠀⠀⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡛⠥⡄⠀⠀⠂⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣨⣭⡥⡶⠿⢿⣋⣭⡜⣿⣿⡟⢺⣿⣯⣽⣿⣿⠁⠀⠀⠀⠀⣽⡇⠟⠰⠂⠶⠆⠈⢻⣿⣿⡿⠛⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⠀⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⣿⣿⢀⣿⠂⠀⠸⠿⡿⢟⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣭⣿⣿⡿⠀⢀⠀⠀⠀⢸⣿⣿⢩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠘⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣌⢿⣿⣿⣿⣿⣿⣇⡁⠀⠀⢹⣿⣿⣿⣿⣿⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠐⡄⠉⠠⡀⠀⠐⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣨⣭⡴⠆⢻⣿⣯⡿⠀⣿⣿⡇⢸⣿⡏⢹⣿⠉⠀⠀⠀⠀⠰⣿⡇⣾⡿⣴⣬⠿⣄⠈⣿⣤⣠⡀⢰⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⡟⣿⠀⣿⢸⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⣿⣿⠈⢻⠊⠀⠀⠐⢠⣾⣿⡿⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢀⠀⠀⠀⢸⣿⡿⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⢛⣿⣿⣿⣿⣿⠿⢫⣷⣿⣿⣦⠻⣿⣿⣿⣿⡏⠿⠂⠀⢸⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠄⢈⣴⣆⠁⢆⡀⠀⠢⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⠃⣀⣴⣦⠁⠘⣿⣿⣧⡄⣿⣿⠀⢸⣿⣧⢸⣿⠘⠀⠀⠀⠀⢀⣿⢇⣣⣬⠵⠋⠓⠀⣀⠸⣿⣿⣿⢸⣿⢹⣿⢿⣿⡇⣿⣿⡿⢿⡿⣿⡇⡿⠀⣿⠸⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠐⠘⠀⠀⠀⠀⠀⡐⠛⢹⣿⠇⣿⣿⣷⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⠀⢹⡀⠀⠀⠀⣿⣷⠀⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⡇⠀⠀⠀⠀⢰⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡝⠟⡿⠟⢁⣠⣼⡿⠟⣩⣵⣷⡙⣿⣿⣿⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢠⣾⣿⣿⣧⡈⠳⡤⠀⠀⠀⠻⣿⣿⣿⣿⣿⡿⢡⡄⣿⣿⣿⣤⡆⣿⣿⣿⠃⣿⣿⠀⣿⣿⣿⢸⣿⡇⠀⠀⠀⠀⠘⡧⢨⡟⣿⣿⣷⣶⣿⣥⠀⠻⠿⣫⢈⡿⣿⣯⢸⡏⣧⡛⣿⣷⡸⣿⣾⡇⠃⢠⣶⡄⣿⢸⣿⣿⢹⡏⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢀⠁⢀⣠⡆⠀⠀⠸⣲⣠⣾⡏⠀⣿⣿⣿⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⡿⢣⠀⣠⡀⠀⠀⠀⣹⡿⣴⣿⣿⡔⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⡟⣿⣿⣿⣿⣿⣿⠛⣿⠻⡿⠁⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡆⢀⣴⠿⠛⣉⣴⣾⣿⢿⣯⣅⣜⢿⣿⡇⣦⡀⠀⢸⣿⣿⣿⣿⣿⠃⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣦⢘⢦⠀⠀⠀⡈⢿⣿⣿⡟⣱⡟⢸⣿⣿⣿⣿⡇⣿⣿⣿⣴⣿⣿⠀⢿⣿⢡⣤⣿⣿⠀⠀⠀⠀⢰⡟⢠⢟⡛⣯⣿⣛⢾⢿⠄⠀⢸⣿⠘⠷⣿⣿⢸⡇⢻⡇⣿⣿⣿⣯⡿⣿⠀⣸⠻⡇⢿⣸⣿⣷⢸⡇⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢀⠚⠂⠴⠀⠂⠄⠀⠀⠐⣿⣿⢷⠄⣿⣿⣿⠀⠀⠀⠀⠀⢸⣿⢻⣽⣿⣿⣿⣿⡀⠀⠈⠉⣿⠃⠀⠀⣿⣧⣿⣿⣧⣟⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⡗⢛⣿⣿⣿⣯⣿⡇⠿⠃⠀⠀⠀⠀⠀⠒⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣦⠊⣠⣴⣿⣿⠿⣋⣥⣿⣿⣿⣿⣮⢻⣧⣿⣷⡄⢸⣿⣿⣿⣿⣿⡆⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣌⠻⡄⠀⠈⠀⠘⠟⣤⠏⠀⠸⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⡟⠀⣾⣿⣼⡿⣿⡏⠀⠀⠀⠀⢸⣷⢰⣏⣻⣿⣛⢥⣠⠄⠂⠀⠈⢿⠐⠇⢸⡇⢸⣿⣸⣇⣿⣿⣿⢹⣿⣿⠀⣿⠐⣧⢸⣻⣿⣿⣾⡷⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⡧⡄⢀⣄⡄⠀⠀⠀⠛⠃⣤⡆⣷⣿⣿⠀⠀⠀⠀⠀⢸⣿⣿⡿⣿⣿⣿⣿⡗⠀⠀⠀⠁⠀⠀⠀⣿⣿⣿⣿⣾⣿⣦⣿⣿⣿⣿⣿⣇⣇⣿⣿⣧⡾⠟⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⠻⣿⣥⣾⣿⣿⣿⡿⠿⢛⣻⣯⣭⣭⡄⣤⣤⣶⣶⣶⣭⣽⣇⡀⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡈⢢⡄⠀⠀⠈⢏⠀⣼⣧⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⡇⠀⣿⣿⣦⣤⣤⡄⠀⠀⠀⢐⣿⣿⢸⣽⢟⣾⢣⣥⣻⣿⠿⡿⡀⠀⢰⣇⢸⣧⣘⢹⡇⢻⣿⣿⣿⢸⣿⣿⠂⣿⡆⣿⢸⣿⣿⣗⣿⡇⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢀⢀⡗⠛⢻⡿⠀⠀⡋⠐⡏⠿⠿⠇⣾⣿⡟⠀⠀⠀⠀⠀⠀⣿⣿⠻⣿⣛⣻⣿⠿⠿⠄⠀⠀⠤⠀⠀⢹⣟⠀⣿⣿⣉⣿⣿⣿⣿⣿⠼⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⢿⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣛⣿⣧⣶⢸⣿⣿⣿⣿⣿⣿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣿⣻⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠙⠂⠄⠀⢂⣼⣿⣿⣟⣿⢿⣿⡇⣿⣿⣿⣿⣿⡇⢀⣿⣿⣿⣿⢸⡇⠀⠀⠀⠀⣽⡿⢸⣿⣿⣉⡚⠛⠻⣶⠖⢣⡶⡐⢸⣿⡏⡛⣿⣾⡇⢸⣿⣧⣿⠈⣿⠿⠀⣿⣿⣿⠈⣿⣿⢻⣿⡇⢹⣿⣿⣿⡇⠀⠀⠀⠀⠀⢸⣿⣇⢀⠈⠁⠀⠈⠂⢠⣧⣴⢂⡄⢻⣷⣷⠀⠀⠀⠀⠀⠀⠻⠋⠠⠐⠜⢛⡁⠀⠚⠀⠀⠈⠀⣀⣠⢼⣿⣧⢸⣿⠿⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⢐⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣛⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣽⣟⣛⠿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⡀⠦⢀⣼⣿⣿⢻⣿⣿⢸⣿⡗⣿⡟⣿⣿⣿⠀⢸⣿⣿⣿⣿⢸⡁⠀⠀⠀⠀⣿⡇⢸⣿⡳⣷⡟⠲⠠⣀⣿⣿⠿⠇⠀⢿⣿⣷⣿⣿⣧⣸⣿⣿⣿⠀⣿⠆⢰⣿⣿⢿⠀⢻⣿⢸⣿⡇⣸⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠿⢿⣀⠄⠈⠉⠁⢸⡇⠀⠙⠃⢸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⡋⢤⣤⡄⣌⡆⣿⣿⣿⣿⢸⣿⡿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⣀⣀⣤⣶⣿⣿⡿⢛⣿⣧⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⠿⠛⢻⣯⣷⣾⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⡷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣡⡿⠁⢀⣾⣿⣿⣿⢷⣿⣿⣸⣿⣿⣿⠇⣿⣿⣿⠀⢸⣿⣇⣿⣿⢸⡇⠀⠀⠀⢨⣿⡇⠸⠿⠇⡋⠁⠐⣒⣫⣖⡀⢀⣠⡄⢺⣿⢹⣿⣿⣿⣼⣿⣿⣿⣆⣿⡆⢰⣿⣿⢸⡇⢸⣿⢸⣿⡿⣿⡟⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠟⠘⠷⠇⠐⠀⠆⠀⠀⠉⠀⠀⢸⣿⣿⠀⣀⡀⢀⣀⣤⣤⣶⣶⣶⣿⣷⣜⡿⢃⣿⡗⣿⣯⣿⣽⠔⠟⠛⠃⠀⠀⠀⢀⣀⣀⣀⡀⠀⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣻⣭⣶⣿⣾⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⢱
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣴⠟⠀⢠⣾⣿⣿⣿⣿⢸⣿⣿⣏⣼⣿⣿⡆⣿⣿⣿⠀⢸⣿⣷⣿⡿⢾⠀⠀⠀⠀⢸⣿⡁⠸⠿⠆⣣⠀⠲⣟⣿⣦⢤⣾⣤⡗⢟⣿⢸⣿⡏⣿⣿⣿⣿⣿⣿⣿⡇⠸⣿⡿⢸⡇⢸⣿⢸⣿⣷⣾⣿⠂⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⢀⣀⣠⡄⢠⣶⣾⣿⣿⣷⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠳⠚⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⣿⣛⣻⣭⣉⣽⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⢿⣻⣾⣿⣿⡶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸
⢻⣿⣿⣿⣿⣿⣿⣿⠟⣼⠏⠀⣰⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⡿⢿⣿⠷⣿⣿⡿⠀⢸⣿⢰⣾⣷⣾⠄⠀⠀⠀⢸⣿⠃⠀⢉⣶⡉⠴⣺⣏⣓⣤⠾⣽⢿⡅⣈⣿⢹⣿⣧⣿⣿⣿⣿⣿⠴⣿⣿⠀⣿⣿⢸⡇⢸⣿⠙⣿⢹⣿⣷⡄⣿⡿⠀⠀⠀⠀⣀⣀⣀⠀⣀⣠⡆⢸⣿⣿⣿⣿⡇⢸⣿⣿⡇⣿⡇⣿⡷⠽⠿⠚⠛⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⢀⣄⣤⣀⣀⣀⣤⡀⣴⣶⣶⢸⣿⣿⣿⡇⠀⡇⢲⡶⣶⡶⢶⣐⣶⣾⣿⣿⣷⣶⣶⣾⣿⣿⣿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸
⠈⠹⣿⣿⣿⣿⣿⢋⣾⠋⠀⣰⣿⣿⣿⣿⣿⣿⡟⠤⣦⡿⢃⣤⣤⣿⢀⣿⣿⣷⠀⢸⣿⠸⠛⠟⠘⠀⠀⠀⠀⢸⣿⡆⠶⣫⣭⣵⣷⣽⡿⡉⣤⣰⣵⢦⣦⣽⣿⢸⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⠀⣿⣿⢸⣷⣾⣿⢸⣧⠸⣿⡿⠃⣾⡇⢰⣶⣾⣿⠋⣿⠣⣰⣿⢾⣿⢸⣿⣿⣿⣿⠇⠺⠛⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⠇⣿⡿⠿⠀⣿⣇⣻⣥⣤⣵⣶⣶⣟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣿⢻⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣾
⠀⠀⠈⠻⣿⣿⢃⡿⠃⠀⣼⣿⣿⣿⣿⣿⣿⣿⡇⢸⣧⠿⠿⢿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣸⣴⣶⣶⠀⠀⠀⠀⢸⣿⡇⠂⣿⡿⣿⣭⣿⢿⣦⣿⣿⢿⣿⡅⣻⣿⢸⡿⣿⣿⣿⣿⣿⣿⡴⣿⡿⠀⣷⢿⠈⣉⢹⣿⡈⣿⡄⠟⣷⡆⣿⡇⠠⣽⣿⣯⠴⠿⠿⠯⠿⠾⠛⠈⠉⠉⠀⠀⠀⠀⠀⠐⠂⠀⠀⠀⢀⣀⣠⣴⣶⣶⣶⣾⣿⣿⣿⡿⠿⠿⠿⣿⣟⣋⣩⣭⣽⡶⣫⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣷⣿⣿⣧⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣦⡀⠀⡀⠉⢡⣿⣥⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣇⣼⣷⣿⣶⣾⣿⡏⣿⣿⣿⣿⠀⣿⡿⣿⣿⣿⠿⠀⠀⠀⠀⢸⣿⡇⣉⡛⣻⣯⣿⢿⣿⠿⠿⡿⢿⣿⡇⢘⣻⣼⡇⢸⣇⣿⣿⣿⣿⡥⣿⠇⠀⠷⠻⠈⠋⠘⠋⠉⠉⠁⠀⠀⠠⠿⠗⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⡀⣠⣤⣤⣴⣶⠶⠾⠿⠿⣿⣟⣋⣉⢉⣭⣽⣷⣶⣾⣿⣿⣿⣿⣟⣯⣿⣿⠟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡿⣿⣿⣿⣿⣿⢸⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣦⡀⠀⠀⡠⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣯⠀⣿⡏⠙⢻⣿⢸⠀⠀⠀⠀⢸⣿⡇⣿⣿⣿⣿⣷⡿⣿⣷⣼⢛⣵⣿⣅⢈⣉⣙⣋⠈⢭⣭⣭⣽⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣠⡀⠀⠀⠤⣤⣦⣤⣤⣄⠀⠴⠾⠿⢟⣛⣛⣿⣭⣭⣭⣷⣶⣶⡿⣧⣿⣿⣿⣿⣿⢫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⢸⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⣿⣽⡟⠓⢖⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢩⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⣿⣿⣾⣿⣿⢸⠀⠀⠀⠀⢸⣿⡇⣪⣭⣭⣿⣿⣿⣯⢝⣫⢿⣿⢿⣭⣾⣽⣹⣿⣧⠀⢻⣿⣿⡿⠇⠀⠀⠀⠀⡀⣀⣤⣀⡀⠀⠀⠀⠀⠌⠿⠿⢃⣀⣶⣾⣭⣭⣭⣵⣶⣢⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣸⣿⣿⣽⣿⣿⣿⢿⣿⣿⣿⣿⣟⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆
⣿⣿⣷⠄⠠⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⣿⣿⣿⡿⣿⣿⣿⣿⣻⣿⣇⠀⣿⣿⣿⠀⠙⠉⠀⠀⠀⠀⣼⣿⣯⡟⣯⣶⣾⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠘⠿⠫⠴⠇⣀⣀⣀⣀⣬⣭⣭⣭⣥⣴⣶⣾⣣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⡟⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⢸⣿⣿⣿⣿⢿⣿⢿⣿⣿⣿⣿⣿⡿⠋⠉⠉⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⡿⠣⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⡿⢇⣛⣹⣿⣿⣿⣿⣯⣤⣿⣷⣶⣔⣓⣀⣀⣀⡀⢀⣛⣛⣃⣟⣿⣷⣿⣷⣿⣭⣭⣿⡿⣻⣭⣽⣭⣭⣷⣶⣶⣶⣾⡟⣣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣾⣿⢸⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⡇
⡿⠃⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣵⣿⣿⣿⣟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣵⣿⣿⣿⣿⣿⣿⣿⣿⢟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣟⣿⣿⣷⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣛⢿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⡿⢾⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣧
⠁⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣵⣿⣏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⡍⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⣿⣿⣿⣿⡇⣿⢿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣧⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⠟⠛⠛⠛⠛⠋⠁⣿⣿⢸⣿⣿⣿⣿⣿⣿⢸⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿
⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣳⣿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣷⣿⣷⢹⣿⣿⣿⣧⣿⣷⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⠿⣋⣵⣶⣦⡤⠀⠀⠀⠀⠘⡿⢸⣿⣿⣿⣿⣿⣿⢼⠃⠀⠀⠀⠀⠀⠀⠀⢛⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣾⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠃⠽⠖⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠰⣼⣿⣿⣿⣿⣿⣷⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣾⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣽⣿⣿⣙⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⡍⣿⣿⣿⣿⣿⠿⣋⠡⣦⣭⣙⡿⠿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣟⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢋⣿⣿⣿⣿⣟⣻⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣯⣿⣿⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⢿⣻⣷⣾⣿⡷⣿⣿⣿⡇⣿⣿⢟⣹⣶⣿⣿⣿⣶⣬⣭⠯⠷⠀⠙⢿⣇⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⠀⠈⣿⣿⣽⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘
⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣛⣽⣿⣯⣝⣛⣛⣿⡈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⠃⠛⠛⠛⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠈⠻⢾⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⢰⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡖⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣛⣛⣛⣙⡿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⢿⣿⠟⢋⣩⣿⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣤⣤⣴⣍⢻⣿⣿⣯⠻⣿⣿⡿⣿⡿⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⢻⣿⣿⣿⣿⢰⣶⣄⡀⠀⠀⠀⠀⠀⠀⣈⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⡟⣿⡿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⡿⠿⠿⣿⣽⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⢿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠁⠈⠙⢿⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⣴⣶⣶⣶⣶⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⡻⣿⣿⣷⣽⣿⣿⣿⠁⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⣿⠀⢿⡇⡇⣷⣶⡄⠀⠀⠀⢠⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⡿⠁⣿⣣⣿⣿⣿⣿⣿⣿⠅⠉⠉⠀⠀⠀⠀⠀⠉⠛⠻⢿⣿⣿⣿⣿⢠⣿⣽⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣾⡿⠟⠉⠀⠈⠉⠉⠛⠻⠿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⡜⠀⠀⠀⠀⠀⣀⣀⣀⣀⣤⣤⣤⣴⣶⣶⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⡿⢳⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣷⡉⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢸⣿⠿⠿⣿⠀⢸⣿⡇⡟⣿⣿⣧⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣸⣵⣿⣿⣿⣿⢸⣿⡿⠟⣫⣭⣭⣭⣉⠻⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡍⠉⠁⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣉⡻⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⢳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠘⣋⣸⢰⣶⣤⣸⡏⣗⣀⢹⣿⣿⣧⠀⠀⣽⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⢧⣇⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡟⣿⣿⣿⣿⣿⡿⠜⠉⠲⠿⠿⣿⣿⣿⣿⣿⣶⡝⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠈⠙⠻⣷⡄⡆⡠⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⣀⣀⣀⣤⣄⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢸⡏⣿⡴⣿⣿⣿⡇⠏⣿⣘⢹⣿⣿⢲⢰⣸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣏⣾⡿⠾⢿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⢣⣿⢿⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠘⢿⣦⣿⣿⣿⣾⡿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠁⠙⠛⠀⠀⠀⠈⢿⡇⣿⣿⣿⣿⣿⣿⠃⠀⢀⣿⣿⠋⣻⣿⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣎⢿⣾⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠸⡿⣸⡇⣸⡺⣿⣧⣾⢹⣿⡌⣿⣿⢸⢨⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣾⣿⢧⣿⡿⠁⢀⣈⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⢸⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⠀⠀⠀⣜⣿⣿⣾⣿⡿⢿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⢿⣿⣿⣿⣿⠇⠀⠀⠈⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢹⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⢹⡇⢻⣷⣿⡏⢿⡆⣿⡇⢿⣿⢸⠀⣾⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⣿⡟⣱⣿⣿⢇⣴⣿⣿⣏⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⠿⢋⣾⣿⣿⣮⣽⣛⣛⣿⣏⢻⣍⡀⢀⣠⡘⢧⠄⠀⠀⠀⣙⣿⣿⣿⣯⣿⣟⣀⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣾⣿⣿⣿⡏⠀⠀⠀⠀⠉⢹⣿⣿⣿⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠸⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢼⠟⠋⠉⠋⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⣏⣇⣞⡝⣿⡗⡘⡇⣿⣷⢸⣿⡇⠀⣼⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⢋⣼⣿⣿⡿⠹⠿⣿⣿⣿⡸⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⢰⣿⣿⣿⣿⡻⣿⣿⣿⣿⣿⣿⡜⢷⣌⠙⣿⡀⢻⡦⠀⢰⡿⢸⣿⣾⣿⡟⣸⣼⣿⣷⡇⣶⢠⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⣀⡾⠿⢿⣿⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣹⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢹⣿⢻⠈⣇⢻⣿⡇⡇⡏⣿⠀⣟⢷⠰⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⠋⠛⠿⠃⠚⠛⠛⠛⠛⣻⣿⣿⣿⣿⣿⣿⣿⣎⢻⣷⡜⣿⣶⠠⠀⢸⠁⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⢇⡏⣾⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡇⠀⠀⠀⠀⠋⠀⠀⣾⣿⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢻⡿⠻⢿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢸⣿⠈⠀⠹⢸⡿⣇⠇⢱⣿⡇⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢿⣿⣏⠀⠀⠀⠀⠀⠀⠀⢸⣿⠿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠼⠿⠿⠿⠿⠟⢛⣛⣻⣭⣥⣭⡁⠙⢿⣦⠀⣿⡄⣿⣿⣿⡟⣾⣿⣿⣿⣿⡿⠚⣸⣿⣿⣿⣿⣿⣿⣷⣦⡄⠀⠀⠀⠀⢹⣿⣿⣿⠁⠀⠀⠀⢰⣶⠀⢀⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢸⣿⢢⠰⡆⠸⠇⣿⣷⣸⣿⡇⣿⡇⠀⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠈⢿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠛⠁⠉⣸⣿⣿⣿⠇⠉⢹⣿⣧⡀⠀⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣾⣿⣿⣿⡆⠀⠀⠀⢸⣿⣧⣤⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠋⠁⠈⠉⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢸⣧⢸⡆⡇⣆⡆⣿⣼⡟⢿⡇⣿⡗⡄⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠐⠂⣈⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢃⠀⠀⠉⠁⣈⠉⢠⡄⢸⣿⣿⣷⣦⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠟⠁⠉⠙⠃⠀⠀⠀⣸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⡞⣾⡇⠃⢿⣿⢸⡟⣿⡜⡇⣿⣿⡅⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀
⠰⠂⢻⡸⣿⡆⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡇⠀⢀⢘⡇⠀⣀⣾⣝⣨⢸⠁⢸⣿⣿⣿⣷⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⣧⢿⣿⠸⠈⣿⢸⣰⠸⣿⣷⠘⣿⡇⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀
⣄⣠⠸⣧⡻⠧⠀⠀⠀⠀⠀⠀⢨⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠠⠸⣿⣼⡇⣿⣿⡿⣸⠀⢸⣿⣿⣿⣿⣧⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢹⡟⣿⢹⣆⢠⢿⣸⣷⡏⣿⣟⣼⣿⡘⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⣿⣿⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠇⣰⡀⠀⣿⣿⣿⣿⣿⣇⠉⡀⣾⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢨⣷⢿⢠⣿⡆⢾⡇⢿⣷⡉⣿⢸⢹⣗⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⣿⣏⣴⣿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⠀⠘⠀⠀⣿⣿⣿⣿⣿⣿⡷⠸⠿⠿⠿⠿⠛⠛⠀⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⣶⢹⣿⣿⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⢸⣿⣼⢀⢻⡓⣌⡻⡆⢿⡇⢿⣲⢸⣧⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⣟⣼⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⢀⣀⡀⠛⠛⠿⣿⣿⡉⠀⠀⠀⠀⡄⢠⡄⠀⡆⢹⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⣿⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠛⠉⠁⠈⠉⠉⠉⠛⠿⡀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢰⢹⣿⡆⢸⡔⣿⡇⣷⡼⣿⢸⣷⡼⡿⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⣺⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠙⠉⠀⠀⠀⢠⣿⣿⡇⢠⣿⣤⣄⠁⣄⣀⢠⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⣿⠨⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⠁⢀⣤⣤⣤⣀⢤⡀⠰⣄⠀⡀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢸⡸⣿⡱⣬⣳⡜⣇⣿⣿⣿⡎⣿⡇⡟⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠛⠛⠛⠻⢿⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡏⠀⢾⣿⠘⠀⠀⣼⣿⣿⣷⡶⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⣿⡇⢿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⢰⠿⣿⣿⣿⠿⣛⣿⣦⡈⣧⡐⡄⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢸⣿⡌⢿⣿⣿⣷⣈⣸⣟⡿⡇⣇⡇⣧⢹⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠈⠁⠀⣤⣤⣿⣿⣿⣿⣟⠸⢿⣿⣿⣿⣿⣿⡆⡄⣽⣿⡿⣟⣻⣟⣛⣛⡍⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣿⣧⢿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠰⠣⣐⠋⠀⠀⠀⠀⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⠀⣿⡷⡞⣿⣿⣿⣻⣿⣿⣇⠐⡇⣧⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢸⣿⡇⣸⣿⣿⣿⣿⢹⣯⢻⣿⡘⣧⢹⣾⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠿⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⡇⢰⣶⣭⣟⡻⢿⣷⠀⢻⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣿⣿⢸⣿⣿⣿⣿⡆⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣻⣿⣿⣇⠤⡄⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⣿⣿⣶⣿⣿⣷⣿⣿⣿⣿⠀⠁⣧⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⠀⠀⢸⣿⣿⡟⢻⣿⣿⣿⢸⣿⡌⢿⣧⣿⢸⢻⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠛⠉⠁⠉⠁⠈⠙⠁⠉⠻⣿⣿⣷⡶⡙⣿⣸⣿⣿⣷⣿⣻⣿⣿⢸⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⣿⣿⠘⣿⣿⣿⣿⡇⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⠪⠖⠟⠍⡩⠅⠈⢀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⣿⣿⠋⣛⡙⠻⣿⣿⣿⡿⠀⢸⡈⠃⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⣿⣧⡸⣷⣿⣿⢾⣿⣿⢨⣿⣹⠸⡜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡄⣿⡏⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⣿⣿⡇⣿⣿⣿⣿⡇⠀⠀⢀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠁⠄⡉⣏⣆⣮⡭⠯⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⡐⠁⠀⢸⡀⠘⢱⣮⡭⣭⣭⠈⢻⣿⠡⠀⢿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⣿⡿⡧⣿⣜⣿⡏⡿⣿⣞⣷⠹⡇⠁⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣷⣹⡇⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⣿⣿⣧⢻⣿⣿⣿⣿⠀⠀⠠⠆⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣤⣶⣶⣿⣁⣉⣻⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢐⠒⠀⠀⠀⠀⢸⡇⠈⢼⡟⣀⣙⡿⣠⣿⠇⣀⠀⣼⠁⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⣿⣷⡇⣿⡿⣿⡿⡇⣿⣜⣿⡄⢷⡆⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⠀⠀⢰⣶⣶⣄⠀⢻⣿⣟⡇⡇⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⡿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠑⣿⣁⠀⠀⠀⢸⣧⣢⠀⢳⣶⣶⣾⣿⠟⣠⢏⣾⣿⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⣿⡟⣿⣿⣷⢻⣧⣷⢹⣿⣿⡇⢼⡇⢿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⡄⢀⣤⣸⣿⠏⠀⢀⢉⣿⣷⣉⢰⣿⣿⣿⠇⣷⣽⣿⣿⣿⣿⣿⣿⢨⣿⣿⣿⣧⣿⣿⡇⠀⠀⠀⢀⢿⣿⣿⢸⣿⣿⣿⣿⠀⠀⠀⣆⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢀⢀⢀⣙⡃⡀⠀⢀⢸⣿⣿⣷⣦⡙⢿⣿⠣⣪⣴⣿⣿⣿⣶⣄⡀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣰⣶⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⡄⢻⣿⣻⢿⣿⣿⢸⣿⣿⡘⢻⣿⣷⡀⡇⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣴⣿⣿⣿⣿⡄⠀⣾⣿⣿⣿⢿⡏⣿⣿⣯⣦⣿⢿⣿⣿⣿⣿⣿⣯⢘⣿⣿⣿⡏⣹⣿⡇⠀⠀⠀⢸⣿⣿⣿⡌⣿⣿⣿⣿⠀⠀⠀⢿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠈⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⢀⣾⣾⣾⡿⠋⠂⠀⢀⣨⣿⣿⣿⣿⣿⠎⠱⣾⣿⡿⡿⢿⣿⣿⣿⣿⣛⡿⣽⣻⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠠⡀⠸⣿⡼⢱⢻⣿⣼⡞⣿⢣⡼⢿⣿⠃⢹⢸⣿⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣿⣿⣿⢻⣿⡇⠀⣿⣿⢿⣗⣞⢡⣿⣿⣿⡟⣸⡌⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⡗⣿⣿⡇⠀⠀⠀⠈⢹⣿⣿⣇⢿⣿⣿⣿⡇⠀⠀⣌⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠉⣛⣿⣿⣿⣿⣿⣿⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠒⠀⣬⠁⣀⣤⣶⣿⣿⣿⣉⣉⣽⣵⣦⣶⣦⣼⣄⣀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣭⣛⢿⣿⣿⡇⠀⠀⠀⠀⠉⢶⡀⠂⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠐⠼⠁⢰⣮⠻⠄⢸⣧⠸⡇⣻⡆⣿⠈⢿⡆⣿⣺⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠰⣿⣿⠟⢩⣭⠀⢀⣀⣈⣈⣂⣼⣸⣿⣿⣿⡇⣾⡇⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⡏⣿⣿⡇⠀⠀⠀⢐⠀⣿⣿⣿⠈⣿⣿⣿⡇⠀⠀⠐⠀⣿⣏⢩⡹⣿⣿⣿⣿⣿⣷⠀⠀⠨⣿⣿⢿⢿⣿⣟⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢀⣠⣴⣾⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣧⡝⣿⡇⠀⠀⠀⠀⠐⠓⠂⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠁⠀⢸⣿⣇⠀⢸⡇⡇⡇⢿⡇⠸⣧⣸⣧⠹⣿⣿⣿⣯⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢰⣾⣿⡿⢨⣿⣿⣿⡟⠛⢻⣿⣿⢸⣿⣿⣿⣧⠛⡇⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣷⣾⣿⡇⠀⠀⠀⢸⡇⣿⣿⣿⠸⣿⣿⣿⣿⠀⠀⠀⡆⢻⣿⣼⣷⡟⣿⣿⣿⣿⣿⠀⠀⠀⠙⡿⣿⣿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣰⣿⣿⣿⣿⣿⣷⡹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢸⣽⢿⡇⢸⣗⠇⡇⢸⡇⡀⠃⣿⣻⠆⣽⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣻⣿⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠛⠛⠂⠀⣿⠉⠉⠁⠈⠈⠉⠁⢸⣿⣿⣿⣿⢰⠀⢻⣿⣿⣿⣿⣿⢸⣿⣿⣽⣿⣿⣿⡇⠀⠀⠀⢸⡇⣿⣿⣿⡇⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⡏⣿⣿⣮⣿⣿⣿⣿⠀⠀⠀⠀⠁⠟⣿⡟⠟⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣸⣿⣿⣿⣿⣿⣿⣿⣷⣹⣿⣿⣿⣿⡿⢿⡿⠿⡟⠛⠛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣽⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢸⣿⢿⣿⡆⣿⡇⠃⠈⣇⢿⣦⢹⣽⠄⢹⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⣠⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⢿⣷⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⣰⣶⣆⢠⠀⣿⠀⣸⣿⣿⣿⣷⠀⢸⣿⣿⣿⣿⠘⠀⣷⣝⢿⣿⣿⣿⢸⣿⣿⣸⣿⣿⣿⡇⠀⠀⠀⢸⣇⣿⣿⣽⣧⣿⣿⣿⣿⠀⠀⠀⠀⠸⣿⡇⢸⣿⣿⣷⡻⣿⣿⠀⠀⠀⠀⢀⣿⣟⣷⡤⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⣿⣿⣿⢿⡙⣿⣿⣿⣿⣧⣯⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣹⣿⣿⣿⢿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠀⠀⢀⡘⣿⣿⣿⡇⢘⠇⠀⢸⣿⡎⢿⡈⣿⣦⠸⣿⣿⣿⠀⠀⠀⠀⠀⠀
⣿⣿⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣼⣿⣿⣿⢿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣿⣿⣿⣿⢸⡿⠀⣻⣿⣿⣿⠇⠁⠀⠙⠻⢿⡿⠀⠀⢿⣿⣧⡻⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⢹⣿⣿⣿⡆⠀⠀⠀⢸⣿⣿⣼⣿⣿⣿⣿⣜⢿⡄⠀⠀⣷⣿⣿⡞⢽⣷⣖⢸⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣿⣿⣿⣿⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⢿⡿⣿⣏⣾⣿⣿⣿⣇⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⣡⣾⣿⣿⣿⣿⣿⣸⣿⣿⣿⣿⡄⠀⣿⣿⣧⣰⡁⣿⣿⡀⣿⣿⣿⠀⠀⠀⠀⠀⠀
⣿⡿⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢸⣿⣿⡿⣧⣸⡇⠐⣿⣿⣿⣏⠀⠀⠀⠀⠀⣤⠀⠀⠀⢸⣿⣿⣿⣜⠿⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢸⡿⣿⣿⣿⣿⢸⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⡿⣿⣿⣿⣿⣿⣶⡃⠀⣾⣿⣿⣿⣿⣾⣿⡿⠘⣿⣿⣿⣿⣿⣿⣿⣿⢃⣿⢣⣿⣿⣿⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣾⣿⣿⣿⣷⣻⣿⣿⣿⡄⠀⠀⠁⠀⠉⠀⠀⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⡧⣿⣿⣿⡏⠉⠀⢸⣿⣿⣿⡗⣾⣷⣆⢿⣿⣿⣻⣧⢻⣿⡇⣿⣿⣿⡆⠀⠀⠀⠀⠀
⣿⡇⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⣸⣿⣿⣷⣿⣿⡇⠸⣿⣾⣿⣿⡅⠀⠆⣤⣴⣿⡀⠀⠀⢸⣿⣿⣿⣿⣷⢹⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢸⣿⢸⣿⣿⣿⠸⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣇⢿⣿⣿⣿⣿⣿⣷⣀⠛⠊⠉⠽⢟⠛⠙⠀⠀⣿⣿⣿⣿⣿⣿⣿⡟⣾⡟⣾⣿⣿⣿⣄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢸⣿⣿⣿⣿⣧⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⣿⢻⣿⡇⠀⠀⢸⣿⣿⣿⠂⣻⣧⢻⣽⣿⣿⡟⣿⢹⣿⡇⢿⣿⣟⡇⠀⠀⠀⠀⠀
⣿⡇⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡟⣾⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠿⠿⠟⠛⠁⠀⠀⠀⣿⣿⣿⡏⣿⣿⠀⠀⠉⠁⣼⣿⣇⣠⡆⠸⣿⣿⡇⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢸⣿⢸⣿⣟⣿⡆⣿⣿⣿⣧⠀⠀⠀⠀⢹⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣦⡀⢀⣖⡖⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⢳⣿⣱⣿⣿⣿⣿⡅⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⠀⠀⢿⣿⣿⣿⣿⡘⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⠘⣗⠀⠀⢸⣿⣿⣿⣰⣿⣿⣿⢿⣿⣿⡇⣿⡈⣿⡇⢴⣿⡿⠃⠀⠀⠀⠀⠀
⣿⣇⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⢸⣿⡇⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠷⣿⣿⡿⢹⣧⣀⣿⣿⡇⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⣼⣿⣸⣿⣿⣿⡆⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⡾⣿⣿⣿⣿⣿⣿⢿⣿⣿⣄⠁⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⡿⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠀⣾⣆⢸⣿⣿⣿⣿⣇⢻⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣁⣿⠀⠀⢸⣿⣿⣿⣟⠏⣿⣿⡾⣿⣿⣿⣿⣿⣿⣧⣻⡿⠀⠀⠀⠀⠀⠀⠀
⣿⣿⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⢻⣿⣿⣿⣷⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⠿⢻⣿⣿⣀⣀⣀⣀⣛⣉⣀⢸⣿⣿⣿⣿⡇⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⣿⣿⡏⣿⣿⣿⣷⢸⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⡇⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣦⡀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣧⣿⣿⢻⣿⣿⣿⡇⠀⠀⠸⠿⠟⠛⠛⠻⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⠿⠿⠿⠿⠆⢹⣿⣿⣿⣿⣶⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠛⠛⠉⠉⠉⠉⠉⣿⣿⣿⢿⠀⠀⠈⣿⣿⣿⣿⡇⠹⣿⣇⣿⣿⣿⣿⢸⣿⣿⠱⣧⠀⠀⠀⠀⠀⠀⠀
⣿⣿⡇⠀⠐⠀⠀⠀⠀⢸⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⣿⣿⣿⣿⣿⠿⢿⣿⣿⠿⠷⢸⣿⣿⣿⣯⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢿⣿⡇⣿⣿⣿⣿⠸⣿⣛⣻⣀⣀⣀⣀⣘⣿⣿⣿⡸⠿⠿⠿⠿⠿⠏⠿⠿⠿⠿⠿⠀⠀⠀⠀⠘⠛⠛⠛⠛⠛⠋⢸⣿⣿⣽⣿⣿⣷⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠈⠁⠀⠀⠀⠀⠀⠀⠈⢹⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣦⠀⠀⠀⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⣿⣾⣿⣿⠨⣿⠀⠀⠀⠀⠀⠀⠀
⣿⣿⡇⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠈⣽⣿⡏⠀⠀⠈⠉⣉⢀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⡬⢭⣭⣭⣉⣭⣥⣬⣭⣭⣭⣽⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣷⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣽⣻⢿⣿⡶⢠⡴⠶⠶⠖⣦⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⢤⣤⣄⣀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠷⠀⠀⢻⣿⣿⢿⣿⣨⣿⣿⡏⣿⣿⣿⣿⣿⣿⢠⠈⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠃⢸⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⠀⠀⠀⠀⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣷⣶⣿⣷⣿⣿⣿⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⢿⢸⣿⣷⣦⣭⣙⡫⠉⠓⠶⣤⣝⢿⠃⠀⠀⠀⠀⠀⢹⣿⣿⣿⣆⠀⠀⣀⣬⣵⣾⣶⣾⣿⣭⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⢸⣿⣿⢾⣿⣿⢹⣷⡇⣿⣿⣿⣿⣿⣿⠈⣐⠀⠀⠀⠀⠀⠀⠀
⠛⠛⠛⠀⠀⠀⠀⠀⠀⠀⠉⢹⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⣾⣿⣿⣿⣛⠉⠁⣾⣿⣿⣿⡏⠀⠀⠀⠀⣿⣿⣿⣿⡇⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣻⣫⣭⣭⣷⣶⣮⣭⣭⣟⡻⢿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣟⢞⠻⣃⣍⣭⣶⣶⣶⠿⠿⠟⣋⣀⠀⠀⠆⠀⠀⢀⡌⣿⣿⣿⡟⣰⣿⣿⣿⣿⣿⣿⠿⠟⡻⠿⣿⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠹⣿⠀⠀⠀⢸⣼⣿⣸⣿⣿⢸⣿⣇⢿⣿⣿⣿⣿⣿⣠⣶⣀⣀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡿⠿⠀⢿⣫⣭⣴⣭⣄⣠⣭⣷⣾⣽⣇⠀⠀⠀⠀⢿⣿⣿⣿⡇⠀⠈⢿⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣴⣿⣿⣿⣿⣿⡿⢛⣻⢿⣿⣭⡻⣿⣦⡹⠿⠟⠿⠗⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⣀⣀⣀⣀⣀⣀⡀⠀⠙⣿⣿⣷⣄⠀⠀⢀⣠⣴⣤⣴⣾⣿⣿⣿⡄⠀⠀⠀⠀⠈⣦⢹⣿⡟⣼⣿⣿⣿⣿⣿⡟⣡⣦⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢿⡆⠀⠀⢸⣿⣿⡾⣿⣿⣿⡏⣿⣸⠹⣿⣿⣿⣿⠸⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣾⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⢟⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣝⠿⠀⠀⠀⠀⠹⣿⣿⣿⡇⠀⠀⠀⠀⠀⠐⣶⣶⣶⣾⡆⢠⣿⣿⣿⣿⡟⣭⣾⣿⣿⡿⣿⣶⣿⣿⣿⣿⣿⣟⠻⣿⣿⣿⣿⣿⣿⣿⣿⡸⣿⣿⣮⡻⣿⣿⣿⣿⣿⣿⡅⠀⠀⣏⣿⣿⣿⣷⣶⣿⣿⣿⢸⣿⣿⣿⣿⣿⡇⠀⠀⠀⣤⡀⢹⣿⣿⢰⣿⣿⣿⣿⣿⡿⢃⣾⣿⣿⢿⣼⣿⣿⣿⣿⡆⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⡇⠀⠀⢸⣿⣿⡇⣿⢻⣿⡇⢿⣿⣇⡟⣿⣿⡿⡗⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣷⡄⠀⠀⠀⠀⠙⢿⣿⡇⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⡇⣿⣿⣿⣿⡟⣸⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣷⡝⠛⠛⠻⠿⢿⣿⣿⡇⣿⣿⣿⣿⣬⢻⣿⣿⣿⣿⡇⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢀⡀⠀⠈⠁⢸⡟⣿⢸⣿⡟⠟⡛⣋⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⢸⣿⣿⡇⣸⡾⣿⡇⣾⡹⣿⡇⣿⣿⡇⡇⣿⣿⣿⡇⠀⠀⠀⠀
⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⣿⣻⣿⣿⣿⣿⢹⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣾⣿⣿⣷⠀⠀⠀⠀⠀⠈⢿⠁⠀⠀⠀⠀⠀⠀⣷⣜⣿⣿⣇⢻⣛⣿⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣽⣟⣛⡻⢿⣿⣝⢿⣿⣿⣿⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡈⣧⠀⠀⡀⠀⠛⠿⠳⠙⢧⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣛⣛⡻⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣍⠄⠀⢸⣿⣿⡇⢿⡇⣿⡇⣿⡇⣿⣿⢹⣿⡇⡇⡿⣿⣿⡇⠀⠀⠀⠀
⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⢛⣟⣛⣛⡛⣙⣛⠍⠉⢍⣉⣉⣉⣹⣿⣿⣶⣶⣤⣬⣿⣷⣶⣿⣟⣛⢿⠟⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⢛⣫⣬⣿⣯⣤⡬⣭⣝⣻⠿⣿⣿⣿⣿⣿⠿⢟⣛⣻⣟⣛⣿⣟⡿⠟⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣶⣾⣿⣿⣿⠀⢟⣙⡛⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⡿⠿⠇⠿⣀⣠⣤⣶⣿⣧⣽⣿⣷⣦⡰⣟⠿⣿⣿⡿⠟⠉⠡⠾⢿⢿⣿⣿⣿⣶⣦⡀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢸⣿⣿⠇⣸⡇⣿⣧⡝⣧⣿⣿⡎⣿⣧⠳⣃⢿⣿⡇⠀⠀⠀⠀
⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⢸⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡞⠛⠛⠛⠛⢿⣿⣶⠄⠀⠀⠀⠀⣀⣛⣠⣿⣟⡛⢛⣉⣴⣾⣿⣿⣿⣿⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣷⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣩⣭⣍⣉⣀⠀⣉⣡⣶⣿⣜⠳⢶⣏⣫⣽⣿⣛⣛⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣿⣿⣷⣘⢿⣿⣷⣿⣿⣿⡿⠿⢟⣋⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣆⢤⣾⣿⣿⣿⣿⡷⢈⣿⣿⣿⣿⣧⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⠈⢻⣿⢠⢇⠇⣿⣿⡇⣿⣿⣿⡇⣿⣿⠀⣿⢿⣿⡇⠀⠀⠀⠀
⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣾⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣚⣛⣛⣛⠒⣷⣷⠶⢄⣀⣀⣠⣶⣿⣿⣿⣿⣿⠏⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣷⢄⣠⣶⣶⡶⠶⠦⠛⠻⠿⣿⣭⣭⣭⠉⠙⠛⡆⠘⠁⣴⣿⣿⣿⣿⢿⣋⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣾⣿⣿⣿⣿⣮⡛⣿⣿⣿⣿⢃⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⣊⣿⣿⣿⢋⣴⣿⣿⣿⣿⣿⣿⣷⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢸⢸⣿⢸⠀⢾⢸⣿⣧⣿⣿⣿⡇⣼⣟⠇⣿⢹⣿⣿⠀⠀⠀⠀
⣿⣿⣿⣿⣇⠀⡄⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣘⣭⣭⣭⣉⢙⣛⡛⢠⣭⣭⣭⣍⣉⣉⣩⣽⣿⡋⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣿⣿⣽⣿⣻⣿⣼⣿⣶⣦⠶⠔⠲⠶⠶⠖⣈⣁⣤⣴⣶⣾⣿⠿⠓⠁⡖⠙⢿⣿⣃⡸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣿⣻⣿⣿⣿⣿⣷⡄⢿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣶⣿⢹⣿⡿⠸⢿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⣿⣿⠸⢸⠀⠀⢸⣿⡌⠼⠈⠌⣯⣿⣿⢻⣿⣏⣿⣿⠰⣿⢸⣿⣿⠀⠀⠀⠀
⣿⣿⣿⣿⣿⠲⣽⣄⢀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣀⣀⣀⣀⣀⣀⣀⣀⣀⣉⣭⣭⣿⣥⣬⣽⣧⠰⠿⠿⠿⠶⠶⠞⠉⠒⠿⠶⠼⠿⠿⠿⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣯⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣻⣟⣘⣛⣛⠋⠉⠁⠈⠀⠀⠋⠋⠉⠉⠉⠉⠛⠋⠉⠁⣀⣐⣚⣓⣉⣉⣉⣁⣙⣛⣛⣛⣛⣛⣛⣛⣛⣛⣛⣛⣓⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣬⣭⣭⣭⣭⣭⣭⣭⣵⣿⣿⣿⣪⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⠆⠁⠉⡉⠉⡍⠛⠛⠛⠿⠿⠿⣿⣿⣿⣿⠙⢧⣿⠀⠠⡀⠀⣸⣿⣿⠀⠀⡂⡸⣿⡿⡇⣿⣿⢻⣿⢰⣿⢸⣿⣿⠀⠀⠀⠀
⣿⣿⣿⣿⣿⡔⠇⡾⠈⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⡿⢿⣿⣿⣿⣿⣷⣶⣷⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⣿⣿⠿⠿⠿⢿⡟⠟⠟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠓⠛⠛⠏⠛⠛⠿⠛⠛⠛⠛⠛⠛⠋⠛⠋⠙⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢹⠀⠀⠹⣇⢠⡀⠀⣇⣹⣜⡀⠀⣧⡁⢹⣷⣧⢹⣿⢸⣿⢠⢹⣾⣿⣿⠀⠀⠀⠀
⠛⠛⠛⠻⠿⠓⠀⠀⠀⠀⠸⣿⣿⢻⣿⣿⣿⣿⣿⣿⡟⠿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠙⠋⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠈⠉⠀⠈⠀⠈⠀⠀⠁⠉⠉⠉⠉⠉⠉⠉⠉⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⢿⠿⠿⠿⠛⠛⠛⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠀⠀⠀⠘⢼⡀⠀⢻⡇⣿⣧⠀⠿⣿⡌⢻⣿⡇⣿⠸⣿⣯⢸⣿⣿⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣧⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⢹⣿⣿⣿⣿⣾⣿⣿⣿⣾⡉⠉⠁⠈⠈⣵⣶⣶⣶⣶⣶⣶⣶⣶⣶⡀⠀⠀⠀⠀⠀⣀⣤⣶⣦⡀⣶⣶⣶⣶⣶⣶⣶⣶⣤⣬⡍⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⡄⢲⣴⡆⢸⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣰⠀⢻⡗⡇⡌⣿⣿⠀⢿⣿⠘⣿⣿⣿⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⢠⣤⣤⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡀⠀⠀⠀⠰⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢀⣤⣴⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣆⢸⠶⠀⠦⠀⠰⢫⠈⢻⣿⣸⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⢸⣇⣿⡝⢣⠸⢸⡇⣧⣷⣽⣻⢇⡽⣏⠟⣿⣿⣿⡇⠀⠀⠀
⣶⣶⣶⣶⣶⡄⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⣀⣄⠀⠘⢻⣿⣿⣿⣷⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢹⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣄⠀⠀⠀⠀⠀⠀⠀⠈⢹⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠈⣿⢹⣷⣼⣧⢸⡇⠇⣿⣎⢻⡏⡇⣿⡄⣿⣿⣿⡇⠀⠀⠀
⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣻⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⠿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⠿⣿⣤⣴⣿⣿⠿⠿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠉⠻⣿⣿⣿⡿⠀⠀⠀⠀⠀⢀⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣟⠀⠀⠀⠀⠀⣘⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⣿⣾⡇⢸⣿⢬⡟⣇⢿⣯⠸⡇⣇⣿⡧⣿⣿⣿⡇⠀⠀⠀
⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⣿⡇⡇⢸⡏⡾⡇⣿⡎⣿⡇⣿⣿⢻⣷⣿⣿⣿⡇⠀⠀⠀
⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡘⡇⡔⢦⠻⡌⣷⢹⣿⣼⣇⣿⣿⢼⣿⣿⣿⣿⡇⠀⠀⠀
⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡆⢛⣾⣷⣿⣌⢸⣿⣿⣿⣽⣿⣾⣿⣿⣿⣿⡇⠀⠀⠀
⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⢧⡞⣿⣏⣿⣿⢻⣿⣷⣻⡼⣿⣸⣿⣿⣻⣿⡇⠀⠀⠀
⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠁⠇⡿⣿⣿⠈⣿⡞⣿⣷⢹⡇⣿⢸⣾⣿⡇⠀⠀⠀
⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣿⣷⢸⣿⣿⣿⣸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠣⣿⣿⡄⣿⣿⡞⣿⣾⡇⣿⢸⣿⣿⡇⠀⠀⠀
⢿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿⢸⣿⣿⣿⣹⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣦⡄⠀⢠⣿⡇⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣷⣷⣿⣶⣶⣿⡀⠀⠀⠀⠀⢰⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡆⠀⠀⢰⣶⣶⣶⡶⢶⣶⡀⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠘⢿⡇⣿⣿⡇⣿⣷⣿⢿⢸⣿⣿⡇⠀⠀⠀
⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣧⠼⢿⠃⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠹⣿⣿⣿⣧⣻⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠂⠀⠀⠀⠀⠀⠀⠀⡀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿⡘⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢻⣿⡿⣿⡇⣿⣸⢸⣿⣿⡇⠀⠀⠀
⠉⠉⠉⠉⠁⠀⠀⠀⠀⢸⣿⣿⣾⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡉⠉⠉⠁⠀⠀⢀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⢟⣽⣿⣝⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⢠⢹⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⡀⢹⣿⣿⣿⣿⣿⢿⡇⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⣤⠸⣇⣿⣷⠹⣿⠸⣿⣿⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣟⣿⣿⣽⢿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣆⠀⡄⠀⠀⢸⣇⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠈⠙⠛⣟⢻⡇⣿⣿⣿⣏⣿⣿⣿⣿⣼⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⣿⣿⣿⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢠⠦⠈⣿⣿⣿⣿⣿⣆⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢹⢰⠌⠻⣿⢠⣿⣘⣿⣿⡇⠀⠀⠀
⣤⣤⡤⠀⠀⠀⠀⠀⠀⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⣙⣿⣷⣧⡀⠀⠈⠁⠀⠀⠀⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠘⠙⠛⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡁⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠘⠀⠀⢿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⢿⣿⠇⣏⣿⡇⠀⠀⠀
⣿⡿⠁⠀⠀⠀⠀⠀⠀⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣦⣤⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢹⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣰⡂⠀⠀⠙⣿⣿⣿⣇⢹⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠻⣧⢿⢿⣇⠀⠀⠀
⠿⠃⠀⠾⠀⠀⠀⠀⠀⣿⣯⣿⢻⣿⡿⣼⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠈⠛⠉⠛⠛⠭⠭⠽⠶⠦⠀⠀⠀⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠉⣻⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⡇⣿⣿⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣷⣷⣿⣿⣿⣿⣿⣿⡘⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠑⠀⠀⡀⠀⠁⢸⣽⣿⠀⠀⠀''', 0.5)
def swamp_art():
    echo('''⣿⣿⡿⢻⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣝⢿⣯⠗⣱⡱⢋⣲⠞⢑⡴⠇⣹⣳⣸⣽⢸⣿⣿⣕⡪⡗⢈⠻⠛⣿⣿⠏⠋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣮⣭⣭⣽⣟⣛⠿⠿⢻⣿⣯⡿⣯⣿⣿⣿⢿⣻⡭⣒⣽⣶⢾⣿⣿⣿⢿⣿⣿⢿⣯⣿⡏⣫⣾⣿⣿⣿⣿⣿⣿⠿⠟⢛⣛⡛⠛⣛⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿
⣿⠟⣱⠸⠿⠿⣿⣚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⣯⡻⣿⣸⣿⠏⣀⡾⠁⢶⠹⠻⢯⣫⠀⠋⠛⡄⠕⢸⣦⢨⣶⠙⠅⠀⠈⠭⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣭⣭⣷⠞⢭⣷⣿⣿⣿⣿⣿⣿⣹⣿⣿⢻⣿⣾⣿⣏⣾⣿⣿⣿⣿⣿⢟⡡⡀⣀⣿⢍⣡⡘⠧⡟⢽⡳⣏⠿⣱⣶⣿⡏⢩⣽
⣿⣲⡜⠈⢻⣷⣶⣳⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⢻⣸⣿⠁⣾⢸⣆⢠⡼⣧⠈⠓⠁⣶⡖⠘⢻⢮⠛⣦⡀⠁⠄⣘⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣽⣛⡿⣿⣧⡟⣿⣿⣿⣿⡾⣳⣿⣿⣿⣿⣿⡿⣷⣼⣟⡼⣻⣧⣜⠽⡆⠉⠰⣷⡝⠛⣘⣿⣿⣿⣟⣿⣿
⣿⣿⣟⣀⣆⣟⣫⣿⣎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣍⠅⠇⢹⠀⢻⣮⡋⢘⡻⠀⠀⣭⡓⠀⠱⠈⠀⡈⢿⡔⠱⣮⣕⠫⢟⣭⣿⡛⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣯⣿⣛⠿⢿⣫⣾⣿⣿⣿⣿⣿⢟⠸⢿⠻⡇⠈⣿⣟⣿⠀⠁⡀⠀⠹⣏⣠⣽⡖⣻⣿⣿⣿⢿
⣿⡿⠶⣠⣶⣶⡆⣸⠏⠜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣅⢶⣰⠈⡜⠀⠀⠡⠦⠼⡺⠓⢠⢡⠀⣆⣿⡔⠁⠀⢘⢿⡟⣕⠲⣅⡙⠺⢿⣐⢢⣽⣭⣟⡛⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠞⠠⣟⣼⢃⡄⣯⣿⣷⡇⢰⢃⠀⢠⣞⣿⣿⣯⢿⡿⠛⣽⣿
⣿⣇⡸⢿⡿⡏⠞⠡⣾⣿⢜⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣷⡘⢓⢻⣿⣿⣿⠃⡠⠀⣼⣾⡆⢿⣿⡼⣧⢨⠢⣔⠈⠃⠂⡀⠈⠃⠲⣽⣽⣗⡓⠮⠎⢙⠼⠙⢰⣤⡍⡻⣛⣻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠘⣾⢿⠁⣼⡇⢹⣿⢙⡀⣰⣏⠀⣘⣿⣿⢿⣻⣾⢣⡾⣿⣾
⣿⣿⠿⠲⠰⠍⢀⠑⠊⠹⣿⣯⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣝⣿⣿⣿⣮⢳⣮⡛⣜⠲⣄⠀⢸⡿⣿⣱⠀⢿⣘⠞⠌⠂⠀⠀⣄⡺⠧⠑⠈⠻⠷⠷⠁⠄⠀⠀⠑⠠⠠⠳⣵⠈⢉⡙⢙⡓⣺⣍⣛⡛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣾⠇⠿⢳⣿⠄⣼⡏⢸⢀⠿⠙⡀⢯⢻⣟⢺⣿⠃⣬⣾⣿⣿
⣿⣿⣿⣿⣿⣧⣶⣶⣮⢠⠀⠉⠯⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣷⡹⣷⠈⠀⠁⠅⠀⢀⠸⠃⠀⠈⠃⠈⠀⢐⢀⡆⠜⠧⣠⡀⢴⣖⠀⣤⠂⢠⣄⡀⠀⣀⠈⠀⠁⣠⡼⠛⠎⠻⣧⢻⠭⠔⡈⣂⣩⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⡹⢲⣼⣾⣿⠰⢛⣴⣾⡟⡁⡰⢶⡌⠉⠛⡟⢃⢰⡿⠋⣿⣿
⢿⢿⣿⣿⣿⣿⣿⣿⣿⠘⡈⡄⠀⠈⠳⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠤⢘⡳⠄⢤⠀⠀⣀⣀⠀⠀⠀⠀⠸⠸⠁⣤⡁⠈⣛⣜⣷⠄⠃⢡⠗⠋⣸⠆⣗⠀⡀⡦⠻⠋⣿⣇⡢⠐⢈⣵⣿⡿⢿⡠⢉⣿⣾⣝⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢘⡘⢛⠙⠣⢬⢾⣿⠍⠘⢳⣃⡔⣂⣼⣷⠁⢁⣏⢑⢿⣿⢿
⣦⣼⣻⣻⣿⣟⣿⢋⣿⣧⠃⢓⢀⣬⣷⡄⡨⡛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣆⢘⢟⠻⣿⣿⢶⠬⢽⠻⢦⣀⡠⠀⠀⢀⣠⡤⣦⠻⢣⠈⠰⡉⢀⠰⡆⠙⣈⠎⠀⠋⡃⡀⠘⣿⢻⠇⣽⣮⣯⣗⡋⣱⣰⣿⣿⡻⣿⢹⣾⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣨⣥⣬⣭⣥⡤⠀⠁⢐⡛⠐⠐⠀⡀⠈⠛⠂⢴⣿⡝⢚⣛⣿
⣿⣿⣿⣷⣭⡿⣿⣸⣿⣿⣿⠎⠀⢻⣿⣷⢸⣮⡪⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢷⣕⠙⢿⣿⣦⣇⡑⠂⠀⠉⡄⠠⣤⣯⣭⡈⢧⠌⠠⠴⢏⡿⣠⣤⢻⣿⡦⠀⠁⠀⠘⠢⣠⠽⡼⣻⠷⣾⣭⠍⡠⣀⣙⡼⢊⣿⣘⠽⠿⣎⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣲⠖⠈⠷⠿⡞⡿⡇⢒⠳⡲⠥⡲⣦⣬⠋⠽⡶⠟⡛⣿
⣿⣿⣿⣿⣿⣿⣷⣿⡿⣿⣵⣦⡰⢰⣟⣿⡇⢿⣿⣎⢑⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠒⣣⣔⣠⠉⣝⡛⠿⠄⢜⣷⣿⡏⢹⢿⢃⣤⣿⣞⡱⠟⢟⠰⠿⢏⡣⣔⠾⠀⣴⠋⡿⣎⠊⠆⢄⢄⡀⢩⣶⢿⢿⡫⢚⣽⣏⣠⠴⠾⢶⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣹⡿⡱⢳⡿⣹⠷⢠⣰⡜⣷⣿⡇⠀⣐⢍⠈⣷⣻⣿⣮⢾
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣷⣿⣼⡿⠟⢱⡸⣿⡇⢈⢇⠻⣺⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣟⣫⡉⠘⠓⠐⠦⠄⠈⠑⠘⣛⡅⠤⠲⠲⠾⠟⢋⣠⣴⣦⢩⡃⠙⠘⠂⠻⢀⡈⠁⢬⣊⢶⣔⡚⡜⣱⢚⣡⢜⢛⡵⠫⣛⣶⣿⣿⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣷⢹⡿⡃⡿⡀⡿⠉⣿⡘⢿⡎⠸⣿⣷⠁⡫⠿⣛⣿⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⡻⣳⡄⣿⠃⢙⠃⢿⣶⣆⢮⣝⢳⣽⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡿⠿⢋⣴⣿⢑⠀⡀⠀⠇⣀⠀⢶⡖⡲⡲⢶⢖⣂⢹⡟⠃⠀⠈⡰⢇⠈⠈⣴⡄⡊⢈⠿⣶⢬⣥⣶⣍⠹⣟⣤⣬⣭⣵⣯⣭⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣾⡏⡟⣑⢡⡇⢡⡞⣄⣷⣷⣼⡗⣀⣹⣿⢤⣻⣸⡼⣫⣾
⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣷⣝⢟⣧⡈⡧⠵⠎⢻⣁⣳⣤⡱⢥⣼⡝⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢴⣿⢿⣞⠋⢄⣵⣷⣶⢏⣫⣤⣇⣖⣜⠁⠸⠏⠇⡁⢶⣀⣰⣏⠸⢀⣵⣍⡷⠖⣋⣈⣛⣿⡿⣡⠵⠶⢣⣦⣥⣼⡽⣟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⡿⡱⢱⠇⣾⣷⢾⢷⠹⣟⣧⠃⢠⣿⠨⣙⣻⣿⢳⣾⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⢿⣿⣿⣷⣍⢿⣷⣠⣾⣦⣰⣿⡋⣾⡿⠋⢱⣷⣷⣝⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢼⣿⣯⠱⣳⡿⠄⢟⣿⣿⣞⣁⣹⡋⠻⣦⣶⣤⢐⠩⣶⣷⣿⠛⣡⡘⢧⣑⣛⣋⡄⣽⠟⣽⡿⣟⣽⡧⣶⡽⢟⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣈⣸⢤⢿⢀⣨⣿⡎⢸⣦⣿⣷⡆⣸⢯⡆⢿⢝⣵⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⣿⣿⡕⣡⣾⠁⣿⣷⣵⣚⢿⣿⣿⣿⣿⣯⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣼⢯⡡⠆⠯⣗⣊⣉⢉⣀⣀⣒⣄⣐⡲⠾⣾⣮⣭⣚⢋⣁⡄⢒⣹⣾⡿⡟⣵⣾⣯⣝⣻⠿⢝⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⢰⣬⢉⡘⣷⣟⣛⠩⣴⢻⣿⣿⣿⣿⣿⣿⡿⣤⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣷⡽⣿⣿⣧⣶⣾⣿⣿⣿⣷⣿⣿⣿⣿⣿⡝⣿⡎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⢿⣻⣽⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣮⣝⡿⣿⢿⣽⡂⠉⢿⣾⠴⣹⣦⡿⢟⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠫⢏⡘⣿⠎⣷⡜⠿⠿⣷⠟⣾⡿⣿⣿⣿⣿⢯⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣞⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣧⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣷⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣟⣿⣷⡿⣗⣪⠿⣻⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣵⡧⣿⣷⠛⢀⠻⣧⣧⢪⣉⣿⢸⡇⣿⣿⡟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣿⣿⣿⣿⣿⣿⣿⣿⣿⡛⢛⣛⣛⡛⢛⣛⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⠶⣍⢫⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣵⣾⣿⡇⣿⣯⡆⢨⠈⣸⣿⣧⣿⣿⢸⢧⣿⢯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣽⣷⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣿⣿⣮⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣿⣿⣿⡿⣿⣭⣷⣶⣿⣿⣏⣼⢰⡿⢏⠁⠜⣿⣿⣷⣾⣽⠿⢿⣿⣿⡿⣿⣿⣾⡏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣵⣿⣿⣿⣿⣧⣿⣿⣧⢸⢠⣾⣿⣿⣿⣿⣜⣼⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠱⣽⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣿⣿⢸⣿⣿⢿⣿⢿⣿⣿⣿⣿⣿⣿⡿⣿⣻⣿⣾⣿⣿⢿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣷⣿⣿⣿⣿⣿⡷⢸⣻⣷⣿⡿⠫⠡⠮⣬⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣩⣾⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⡌⣾⣿⣿⣿⣿⣿⣮⣿⣿⣾⡻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣧⣻⣿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡞⣿⣾⣿⣿⣼⣿⣯⠉⣉⢩⣭⢩⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣫⣵⣿⣿⣿⣿⣿⢵⣯⣏⡓⣔⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣯⣿⠋⣼⣿⣿⣿⣿⣿⣿⡸⣿⢸⣿⣿⣓⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣟⣛⣿⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣷⢿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⣿⣿⣿⣿⣿⡏⣿⣿⡇⣼⣿⣿⡿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣯⣴⣿⣿⣿⣿⣿⣿⣿⣿⣟⣯⢭⣭⣿⡇⢨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣯⣾⣿⣿⣿⢠⣿⣿⣿⣿⣿⣿⣿⣧⣻⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢹⣏⠃⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣎⣾⣿⠣⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⣾⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣧⢻⣿⠞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⣚⡟⠿⠇⢣⣿⣿⣿⣿⣿⣿⣿⠿⣻⣵⣿⣿⣿⣿⣿⣿⣿⣿⡇⣾⣿⣿⣿⣿⣿⣿⣿⣆⢿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣾⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠐⠋⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⡻⡇⡿⠇⢸⣿⣿⣿⣿⡿⣯⣷⡏⡿⣱⣿⣿⣿⡿⠿⣿⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⡇⢸⣿⣿⢫⣽⡎⢩⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⠃⣼⠀⡇⣸⣿⡿⣿⣵⣿⡿⢿⡓⣘⣭⣷⣶⢾⣫⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣶⣾⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢠⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡿⠇⣴⣧⠀⣿⣿⢸⣿⡇⢸⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣛⣵⠀⠛⣤⣷⢿⣫⡾⠿⣛⡑⣋⢼⡟⣹⠽⠋⣁⣿⣾⣴⣶⣿⢇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢼⣿⢯⣿⣶⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⡆⣿⣿⣸⣿⡇⢸⡼⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⡏⢰⡇⣿⣵⣿⣯⡞⢁⡿⣿⣅⡽⡋⢽⣽⢀⣿⡟⢱⣿⣿⣿⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⢿⣷⣜⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢷⣾⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣿⣿⣿⡇⢸⣿⢿⣿⡇⢸⡍⣿⣿⣿⣿⣿⡿⣟⣛⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⡇⠉⡷⣿⠋⠛⣿⢀⣿⣿⡿⠟⠁⠀⡼⢟⢸⡟⠀⠐⣭⣷⡿⢸⣿⣿⣿⡏⢿⣿⣿⣿⣿⣿⣿⣿⡏⢷⡺⢿⡏⣧⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢊⣾⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠹⢿⣿⣿⠀⣿⣼⢸⡇⢸⡇⣿⣿⣿⣿⡿⢿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣸⣿⢼⡅⣷⡶⣼⡇⠀⢢⡭⠉⠀⠀⠀⠀⣿⡜⡟⢠⣾⣿⣺⣥⡷⢈⢿⣿⢫⣾⣷⡹⣿⣿⣿⣿⣿⣿⣇⡽⣷⣸⢿⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣻⣽⣿⣿⣿⣿⡿⢿⣻⣿⡛⠛⣯⠻⢟⠿⢛⡛⠟⠛⢿⢿⢇⢸⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢡⠌⣛⡇⢻⢹⢸⡧⠈⣷⣿⡿⢛⡑⢘⢇⣸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣹⡇⢸⡇⡇⠑⣭⡅⣼⣾⠂⣠⣦⠳⣄⢶⣤⣅⣥⡬⣿⣿⣿⣿⡇⣿⢸⣿⠸⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣷⣿⣯⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢿⣟⣫⣭⠽⣶⣯⣭⣩⣉⣷⣾⣿⣿⠷⠟⢏⠻⢿⣭⢫⡵⣦⠄⠅⠲⡌⢦⢫⡛⢀⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢰⣿⣿⣧⢸⡌⢞⡝⠀⢱⠛⢡⣾⢃⣿⣷⢨⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⡇⣠⠔⢈⡃⣿⡄⣡⡥⢋⠳⣄⣿⣿⡆⢊⡋⢹⣿⡇⠀⣿⣷⣿⣿⢧⣯⣿⡇⣿⣧⢹⣿⣿⣿⣿⣿⣿⣿⣿⡜⣼⡟⣾⣷⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣭⡍⣷⣶⣶⣿⣿⣿⣿⣿⣿⠟⢑⣋⢴⣿⣼⡿⠃⢴⢟⣷⢴⡿⠡⠿⠋⣰⣶⠸⣧⣤⣤⣬⢻⣆⢟⡊⢣⣾⣿⣿⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⣿⣿⠀⠃⢸⣷⡀⠸⠃⡲⡁⣼⢿⣿⣸⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡇⣿⢠⣧⡳⠘⡏⡿⠁⡿⠀⠊⠓⢹⣧⣿⠧⢸⡏⢁⣀⠽⣿⣿⢏⣾⣿⣿⣇⠿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣹⣿⢿⣿⣿⡞⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡼⣿⣿⣿⣿⣿⣿⡿⣱⣰⡿⣣⡟⣽⡟⢉⣰⣷⡿⣫⣾⣷⡿⢋⡂⣰⡅⠱⣿⡦⡲⠇⣦⢻⣿⢅⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣋⣵⣿⣿⣿⣽⣍⢝⣛⡿⢶⣶⣦⣖⣂⣤⣬⣙⣛⣻⠩⢭⣱⣾⣿⣚⣷⣭⣭⣭⣭⣭⣭⣥⣵⡾⣽⡇⡇⢹⡇⣸⣧⣆⡫⡱⡌⠛⣽⠇⢼⢻⣼⣿⢠⣿⡟⢸⡟⣉⠄⡙⢱⡏⣤⡍⣿⣙⢯⡻⣿⣿⣿⢹⣧⣿⣿⣿⣧⢧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣭⣙⣓⣙⣿⣿⠿⢿⡿⣃⣴⣿⣐⠭⣵⡿⡰⠏⣼⣿⢣⣿⣿⡏⣾⣟⢁⣿⣿⡎⣮⡙⣥⡀⣛⠭⠁⣼⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣭⣿⣿⣿⣷⡶⢂⢤⣾⣿⣿⣿⣯⡿⢿⣿⣿⣿⡷⢾⣿⡇⣿⣟⣭⣭⣭⣙⣛⣛⠿⠸⠇⠾⡇⡇⠀⣰⡎⣿⣿⣿⣿⡌⡄⡟⢸⡈⢰⣿⣿⡎⠙⠄⢸⢇⣵⣶⡹⡄⢃⣿⠈⡕⣵⣷⣭⣎⢻⣿⡟⣿⢜⣿⡝⣿⡾⣿⣿⣿⢿⡿⢿⣿⣿⣿⣿⡿⣿⢿⣿⣿⣿
⣿⣿⣶⣶⣿⣿⣿⣿⣯⡷⢾⣿⡿⠿⢿⣿⣿⣿⣿⣷⣶⣖⣲⠶⢾⣶⣾⣷⣷⣮⣿⣧⣽⣱⣽⣯⣵⣂⣸⣟⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣷⣶⣿⣿⣿⠷⣶⣶⣶⡹⣷⣾⣿⣾⣶⣾⣶⣭⣽⣷⣲⢼⣿⡇⣿⣿⣿⡿⣬⣿⣿⣿⣿⣿⢿⣿⣿⣷⢶⢖⠶⣿⠯⣭⡩⡭⠤⣄⡘⠁⣿⣶⣷⣦⡏⡄⡟⣸⣯⡇⣧⣾⠈⡟⠸⢸⣿⣿⡜⢿⡜⣿⣧⣿⣎⢜⣯⣿⣇⣟⣿⣿⣟⣵⣞⠌⠇⡺⢡⣾⣷⣿⣾⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣯⣿⣻⣾⣾⣭⣿⣛⣛⣛⣻⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢷⣿⣿⣿⣟⣛⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣟⣵⣿⣿⣿⡿⣿⠧⣿⣿⣿⣿⣻⡿⣋⣫⣿⣿⣿⣿⣿⠇⣿⢻⡹⡇⢘⡻⣿⣿⣿⣿⣿⣿⣿⣟⣷⣧⣿⣾⣻⣿⣫⢼⡟⣼⡇⡄⣿⢿⣿⢻⣿⣿⢱⣿⢸⡇⣿⣿⣧⣃⣧⣺⣿⣿⣿⣿⣷⣿⣿⣿⣿⡌⠿⣿⣿⣸⢻⣿⣿⣿⣿⡇⢸⠀⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣷⣿⣶⣽⣭⣿⣻⣿⣻⣯⣾⣿⣿⣿⣿⣿⣿⣿⣾⣯⢹⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣻⣿⣿⣿⡿⢿⣿⣿⢻⡷⢸⣿⣿⣿⣿⡶⠟⣶⣌⡻⣿⢾⣿⣠⣯⢸⣳⡰⠈⣥⣿⣶⡛⣿⣿⣿⢻⣿⣿⣿⣿⣷⣿⣷⣿⣟⣯⣿⡇⢼⣿⢸⣿⣿⡟⠃⢞⣟⣏⢿⣿⣿⣿⣿⣇⣷⡸⣿⣿⣿⣿⣿⣿⣿⣿⣷⢰⡹⣿⡏⡼⣿⣿⣿⣿⣧⣼⢰⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⡿⣿⣟⠿⣷⣿⡿⣶⣮⣻⣿⣷⠹⣾⣯⣯⣿⣿⣿⣿⣿⣿⣷⣿⣿⡿⢶⣿⣿⣛⡻⠿⢿⣿⡿⣿⣿⣿⣼⣿⣿⣿⣷⣶⣯⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠯⣿⣫⢉⣿⣭⠭⣰⢻⢸⣿⣿⣿⣿⣿⡶⢂⣀⣿⣮⣼⣿⡟⣿⣸⢰⡆⣀⡠⣴⣿⣿⣿⡿⢿⡾⢿⣿⣿⣿⣿⣿⣹⡿⠿⣹⣿⣿⣜⣿⢸⣿⣿⣧⣶⣬⣭⣭⣧⣭⣭⢹⣿⢫⣤⣧⣭⣭⣯⣭⣭⣭⣭⣭⣭⣭⣥⣯⣭⣭⣭⣭⣭⣭⣭⣿⢸⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣗⢿⣿⣿⣿⣿⡃⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡿⣿⣾⣿⣿⣿⣟⣙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣮⢻⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣼⣿⠿⢏⢹⢟⣫⣾⢸⣿⣿⣿⢿⣷⣿⣿⡜⢿⠿⣿⢿⢸⣿⣿⣶⡓⡌⢿⡿⣿⠟⣻⠢⠟⡑⡜⣿⣿⡿⣋⡝⡟⣳⢾⣣⣿⣿⡟⣿⣼⣿⣿⣏⡛⢛⣟⣛⣛⣛⣛⢸⣿⢸⣿⣿⣿⣻⣻⣿⣟⣛⣻⡿⢿⣻⣭⣭⣭⣟⣻⣯⣍⣛⣋⣉⠘⡛⣻⣟⡻⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣮⣿⡿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣬⣟⣿⣿⣯⣽⣻⣿⢸⣿⣿⣿⣿⢻⣿⣿⣿⣧⢿⣿⣿⣿⣿⣿⣷⣿⣿⣿⢸⣿⣾⣿⣿⡿⣿⣿⣧⣽⣿⣿⣼⢸⣿⣿⣿⣷⣭⠘⣿⣯⡅⣿⣿⣷⡼⣝⢿⣻⣿⣏⣥⣾⣷⣿⣿⣿⣿⣇⣿⣻⣿⣿⡽⣿⣷⣶⣿⣿⣿⣿⣤⣥⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢿⣩⣾⣿⣿⣿⣿⣿⣿⢿⣾⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣝⡿⣿⣿⡿⢸⣿⣿⣿⣿⢸⣷⣯⣻⢿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⣿⣿⣿⣷⣽⢿⣿⢸⣿⡟⣿⣿⣿⣷⡜⣿⣿⣦⣝⠟⣡⡝⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⢸⣿⣿⡇⣛⣛⣛⣛⣛⡛⠛⠛⠛⠛⠛⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠿⠿⢿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣛⣻⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⢿⣷⣽⣿⣿⣿⣿⣿⣿⣻⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣻⣿⣮⣟⢿⣸⣿⣿⣿⣿⢨⣿⣟⣿⣷⣾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣮⡻⣿⣻⣾⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣟⣻⣿⣿
⣿⣿⣿⣿⣿⡻⣿⣿⣿⣷⣾⣿⣶⣾⣷⣿⣷⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣷⣧⣝⡻⢿⣿⣼⣿⣻⣿⣿⣿⣷⣮⣭⣛⡿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠿⣿⣽⣿⣿⣛⣛⣫⣹⣿⣿⣿⡯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣛⣯⣽⡾⣟⣛⣯⣭⣷⣿
⣿⣿⣿⣿⣿⣿⣯⣿⣯⣿⣻⣻⣿⣽⣿⣽⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣞⡿⣿⣿⣮⡿⣿⣿⣿⣾⣝⣿⡷⣾⣭⡻⠇⠿⢿⣾⣽⣭⣭⣿⣿⣿⣿⣿⡿⣌⣫⣭⣝⣻⣗⣲⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣶⣶⠶⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣾⢿⣿⣯⣻⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⣿⣿⣿⣿⣿⣿⣷⣿⡻⣿⣿⣿⣿⣿⣿⣾⣻⣿⣿⣿⣿⣿⣿⢿⣷⣯⣛⢿⣷⡽⣯⣿⣷⣿⣻⠷⣯⣿⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣟⣛⣽⣿⣿⣟⣿⡾⣿⣻⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣝⣿⣿⣿⣿⣿⣿⣻⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣽⣿⣿⣻⣿⣿⣍⣯⣽⣛⣛⣭⣭⣭⣭⣭⣭⣓⡛⢻⡭⣭⣭⣭⣭⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣟⣻⣿⣿⣿⣿⡿⣻⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡾⣿⣭⣿⣿⣿⣷⣽⣻⢿⣿⣿⣿⣿⡿⣿⣟⡷⠽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣾⣭⡻⣿⣿⡿⣿⡟⢿⣿⣷⣿⣽⡿⣷⣿⣯⣿⣿⣿⣯⣿⣿⣿⣦⣭⣭⣭⣭⠿⢟⣛⣿⣿⣿⣿⣿⣿⣟⣋⣭⣍⣙⠛⠻⢿⣿⣿⣿⣿⣭⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡱⣿⣿⣿⣿⣿⣿⡟⣼⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⡿⣾⣻⣿⣟⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣾⣿⣿⣾⣿⣷⣝⡿⠿⢿⣿⣷⣿⣣⣛⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡋⠷⠾⢗⢉⣱⣿⣟⣿⣿⣿⠿⢅⣿⡷⣿⢿⣿⣿⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣯⢿⣿⣿⣿⣿⣿⣽⢿⣿⣽⣿⣿⣿⣿⣻⡿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⡿⢿⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣟⣛⣛⣿⣛⣛⣛⣛⣛⣛⣛⣛⣛⣛⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⢻⠭⢟⣛⡩⣥⣼⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢿⣿⣟⢿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣮⣿⣿⣿⢟⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣐⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠋⢉⡮⠇⣒⣀⣒⣲⣾⣟⣛⣯⣭⣭⣭⣝⣛⠻⠿⠿⠿⠏⢽⣟⠿⣿⣿⣿⣷⣽⣮⡳⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣭⣻⢿⣮⡾⣿⢿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣝⢿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢟⣛⡯⠽⣢⣭⣵⣴⣿⣿⣿⣿⣾⡌⠛⠛⠛⠛⠛⠋⠉⠉⠉⠉⠉⠛⠛⠛⠛⠛⠓⠐⠿⢷⣶⣶⣶⣶⣹⣿⣮⡳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣻⣿⣿⡝⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣶⣦⣷⡞⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣟⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢸⣿⣿⣟⠪⡻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⠿⣛⣿⣿⣯⣭⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢘⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣾⣯⢂⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣯⣿⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⢸⣿⣿⣿⣿⠿⣛⣻⣯⣯⣶⣾⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⡀⠀⠀⠀⠀⠀⠀⠸⡿⣿⣿⣿⣿⠘⢸⣷⡿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⡟⠿⣋⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠈⢿⡾⣿⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠈⠀⠀⠀⠀⠀⢀⣾⣮⡻⣻⣿⣿⡆⣾⣿⣎⢻⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⡿⠿⠹⢃⣤⣯⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣛⣯⣭⣤⢁⠋⣧⢿⣿⣿⣿⣿⣿⣿⡿⠿⣟⣻⣯⣭⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣷⣶⣶⣶⣶⣦⣤⣄⣀⠀⠀⣾⣿⣿⣿⣾⣿⢫⢠⣿⣸⣿⣷⣝⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣴⡆⣷⣿⡇⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⢿⣿⣿⡰⢿⡸⠿⣛⣯⣽⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡹⣿⣿⣿⣿⠘⢸⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢛⡍⣿⣿⣿⣿⣿⣇⢌⢩⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢟⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣿⡇⡇⣇⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⣾⡿⢛⣥⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣝⢿⡏⡇⣶⣜⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠞⢠⣿⣿⣿⣿⣿⣿⣯⠄⠋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢟⡽⣯⠀⢂⣪⣇⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⠃⣷⢹⣿⣿⡿⣟⣻⢩⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠩⠿⠿⢿⣟⣛⣛⣟⣛⡛⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣃⢀⣿⣿⣯⢻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢠⢺⣿⣿⣿⣿⣿⣿⠳⣼⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢛⢫⢹⢐⣮⣣⢳⣾⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⢀⢸⢨⣭⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣣⠉⠙⠛⠛⠛⠒⠒⠲⠶⠶⠿⢯⣥⣭⣤⣀⣀⣚⣛⣛⡻⠽⠭⠭⠿⠿⣿⣿⣻⣻⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣮⢟⣿⣿⣷⡿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠸⡇⢿⣿⣿⣿⡿⡣⠍⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣛⠩⢵⢂⠔⣿⢫⣱⢧⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣟⣯⣷⣶⡜⠸⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⡟⠭⠟⣊⣩⣭⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠙⠛⠛⠛⠿⠶⠶⠶⢶⣶⣦⣭⣭⣭⣭⣛⣛⣛⣛⠟⠝⠟⠫⠭⠭⠁⣶⣿⣿⣿⣽⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣅⣒⣮⠙⡛⢉⣨⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣿⢽⣿⣻⠁⣿⢻⣟⣿⡶⢾⢘⣎⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⡹⢻⣘⣻⣭⣿⣿⣿⣿⣿⣿⣿⡇⠀⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣛⣥⣶⢾⣿⣛⣿⣷⣿⡆⢤⣴⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠛⠛⠻⠛⠳⢰⣿⣿⣿⣿⣿⣞⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣗⢿⠿⠿⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣿⣾⣿⢯⡇⢸⠀⠈⣯⣿⣾⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣓⢿⢩⠭⠋⣭⡔⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⡆⣿⢿⣿⣿⣟⣫⣿⣿⢟⣽⣿⡿⢽⣷⣽⣿⣯⣽⣶⣿⣿⣿⣿⣿⣿⣿⡜⣿⠘⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢬⢺⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣛⣭⣽⣶⣶⣶⢻⣿⣸⣿⠿⣟⣯⣿⣶⣿⣿⣿⣿⣿⣿⣿⣆⣾⡇⢸⡀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢽⣟⢊⠁⣍⣃⣠⣣⣼⢻⣷⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣧⣤⢻⣼⢿⣷⡿⢿⣻⣽⡛⢽⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡉⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⣾⠀⠈⣻⣿⣿⣿⣿⣿⢀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣱⢿⣿⣿⣿⡿⢟⠛⢬⣑⣰⢺⣏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⣇⠇⣿⣿⣿⣿⣿⣿⢟⢛⣋⣉⣰⣿⢾⣟⣯⣻⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⠿⣛⠧⣻⢸⡟⣩⠶⣛⣻⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣯⣕⣛⣫⠴⣂⠀⠀⠀⠀⠀⢫⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣜⡖⡰⣹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣼⠫⢟⣛⣩⣭⣶⢟⣶⢛⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⡿⢀⢾⣿⠿⣻⣭⣶⣾⣿⣿⣿⣿⣷⢿⣿⣿⣿⣿⣿⢿⣯⢹⣿⣿⣿⣿⣿⣿⣿⣬⣥⣤⣬⣤⣀⣘⠎⢷⠍⢭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣯⣽⣶⣶⣾⣿⣧⠀⢰⡆⣤⣆⢹⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣯⣿⣝⠜⠘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⠻⠍⣥⢴⣎⣿⣸⣿⣿⣏⣿⣿⡇⣿⣿⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⠿⣟⠟⠀⣤⢸⣨⡄⣾⣿⣿⣿⣿⣿⣿⣿⡿⣲⣿⣿⣯⠹⠷⠾⢮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣾⣶⣯⣿⣿⣿⣿⣿⣻⣿⣿⡿⠿⠿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠼⢻⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠠⣨⣿⣿⣿⣿⣿⢸⣇⠟⣽⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣛⣿⣿⣟⣻⣯⣽⡾⣣⣾⢣⣧⣿⢤⣾⣳⣿⣿⣿⣿⣿⣿⣿⢸⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⠿⢏⣸⣾⣯⣴⣦⢸⢿⢸⠆⣿⣿⣿⣿⢿⣟⣿⣿⣿⠺⠛⣭⣅⣒⣛⣛⡿⠿⢶⢾⣷⣿⣭⣟⠿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣽⣿⣟⣉⣛⣀⣀⠀⠀⠀⠀⢀⣀⣀⡀⣀⣀⣀⢀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⢀⠀⢀⡇⢿⣿⡟⣿⣷⣟⣿⣿⣿⣼⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣯⣿⡶⢛⣫⣽⣷⣿⡿⣛⣯⣽⣾⣿⡟⣸⣿⣿⣟⣥⣻⣿⣿⣿⡟⣿⣻⣿⣧⢿⡇⣿⣿⣿⣿⣿⡿⢿⣷⣿⣿⣿⣿⣿⣼⢷⠘⠸⡏⡇⣟⣿⣿⣷⣿⣿⣿⠿⣙⣼⡇⠂⠋⢩⠭⠭⣙⣘⡒⠲⠠⢶⡮⣭⣵⣦⣈⣛⠿⠿⢿⣿⣿⣿⣿⣛⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣭⣭⣭⣭⣿⣟⣛⣛⡻⠷⠂⠀⣂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢡⣿⣿⠀⣿⢷⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⢿⡉⢟⢉⣒⡆⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⡿⣵⣿⣿⢏⢾⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⡼⡇⣿⠏⢻⣿⣿⣇⣾⣿⣿⣿⣿⣿⣿⣿⠜⡂⡁⡇⣇⣿⣿⣿⣿⣿⢟⣫⣽⣶⠾⠟⠋⠁⠀⠈⠀⠈⠉⠙⠛⠛⠿⠶⠶⣦⣬⣭⣭⣽⣟⣛⣲⡒⠶⢶⣶⣾⣭⣭⣵⣶⡒⣒⣾⠭⠵⢭⢿⣿⣿⣽⣟⡛⢿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣤⣤⣤⣄⣀⣀⣀⠰⠣⠿⣿⣿⣧⠹⣏⣮⢻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣧⢻⢸⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣾⣿⡿⣫⣵⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣧⠃⣿⣤⣾⣿⣿⣿⣿⣿⣿⣿⠿⣶⣏⣵⣾⡇⢖⢧⢹⢹⢿⡿⠿⠞⣑⡯⢽⣶⣾⣷⡀⠀⠀⠀⠈⣄⠀⠀⠀⠀⠀⠐⠛⠁⠀⢀⣭⣽⣿⢟⠭⣹⢿⡟⢓⣂⠒⠐⠈⠁⢩⣍⣍⣭⣟⣛⣿⠶⠠⡿⠯⣿⢽⣟⣛⣻⣿⠿⠿⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣮⣥⣽⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⢸⣼⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⡆⣿⣏⢿⣿⣿⣿⣿⢿⣫⣵⣿⣿⢿⣿⣿⣷⢿⠸⢼⠐⠪⠤⢒⣩⣜⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⢸⣆⠀⠀⠀⠀⠀⠀⠀⠀⠘⢛⣿⣿⣷⣿⣻⣭⡼⡟⢚⣌⡤⡵⡀⢶⣰⣦⣭⣭⣭⣟⣛⢻⠿⠿⠶⠦⣭⣭⣭⣉⣛⣛⣓⡶⠶⠿⠷⢭⣭⣟⣿⡿⣟⣛⣻⣿⢿⣷⣿⣭⣭⣿⣿⣿⣟⣛⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⢻⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣾⢯⣷⣿⣿⠿⣋⣵⡿⢿⡩⢌⠈⡀⢈⣷⢶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠘⣄⠀⠀⠀⠀⠀⠀⠀⢀⣴⡐⣿⣿⣿⢿⣫⡥⣶⠃⣱⠶⢨⡻⠌⢳⣿⠿⣟⣻⣭⣶⣷⠾⢻⣿⣿⠖⣤⣶⣾⣭⣭⡿⢛⡛⢓⡶⠶⠾⢷⣯⣬⣭⣭⣛⣛⣒⠲⠶⢶⠿⣯⡭⣭⣿⣻⣟⣿⠿⠿⢿⣶⣶⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠗⣫⣵⣷⣶⣿⢿⣋⠴⢛⢡⣣⣬⣵⡜⡜⣯⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣧⠀⠀⠀⠀⠻⡄⠀⠀⣀⣀⣤⣴⣿⣿⣷⡘⠿⢟⣫⡷⣟⣧⣶⣷⣶⢞⣯⣿⣾⢿⣿⣿⣿⠿⠋⠃⢁⡾⢛⣴⣿⣿⣿⠟⡵⣠⡾⢋⣴⣿⣳⣿⣿⣿⣶⡶⣖⡭⣩⣭⣛⢛⣛⡷⠶⠶⠦⣤⣵⣮⣙⣫⣽⣻⡿⠷⠶⢾⡯⣿⣟⣛⣛⣓⣶⣿⠿⠿⠭⣭⣟⣫⣛⣟⣛⣻⠻⣿⣿⠻
⣿⣿⣿⣿⣿⡇⡇⣿⢸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣻⣽⣾⣿⣯⣾⣯⣿⣿⣿⣯⡇⢹⡹⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢀⣀⠀⠀⠸⡄⢀⣾⣿⣿⣿⣿⣿⣿⣧⡈⣿⣷⣿⣿⣿⠿⣻⣵⣟⣯⣿⣿⣿⣿⣯⡷⠞⠀⠿⣨⣽⣿⣿⣿⣿⢗⣺⠞⣋⣤⢟⣽⣿⣿⣿⣿⡿⢋⣾⣿⣿⡿⡫⣳⣾⣿⣿⣿⣿⢖⡶⢠⣔⡭⣭⣭⣿⣛⣛⣿⠷⠶⠶⢦⣽⣽⣭⣿⣋⣛⡻⠟⠺⠾⢩⣽⢭⣭⣿⢟⣛⣻⣿
⣿⣿⣿⣿⣿⣷⣧⣿⢸⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⢿⣻⣭⢶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣧⠙⣿⣿⣿⣿⣿⢿⣫⢽⣻⣭⣶⣿⣎⢿⣧⠀⠀⠹⣌⣻⣿⣿⣿⣿⣿⣿⣿⣧⠜⠿⢛⡉⣐⣻⠿⢿⣿⣿⡿⢛⣭⡿⠋⣠⣴⣯⣾⣿⣿⣿⠟⢉⣵⡾⡋⣸⣟⣵⣾⣿⣿⣿⡿⢋⣴⢟⣙⣩⢍⢞⣴⣿⣿⣿⣿⡿⣯⠟⣠⡿⢏⣽⣿⣿⣿⣿⣿⢿⣿⢃⣾⣷⣶⣬⠻⣿⣛⠛⠛⠿⠿⡟⠲⠶⠦⣾⣼⣯⣭⣭⣭
⣿⣿⣿⣿⣿⣿⢿⢸⢸⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣟⣩⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣰⡾⡇⢹⣿⠿⢶⣪⣵⡾⣛⣷⣿⣿⣿⣿⣎⢿⣧⠀⠀⢹⣋⣽⣿⣿⣿⣿⣿⣿⡿⠇⣐⣭⣾⣿⣿⣿⣿⡿⠂⣠⣼⠩⡠⣚⣛⣿⠿⠿⠿⠟⣅⣴⠟⡫⣊⣶⣿⣿⣿⣿⣿⡿⠋⣴⢟⣵⣿⣿⣿⢏⣿⣿⣿⣿⡿⢫⡾⢵⣯⠎⣴⣿⣿⣿⣿⣿⣿⣣⡿⢡⣾⡿⣻⣿⣿⣷⣝⢿⣷⣦⡀⠀⠀⠈⠻⢃⣷⣶⣾⣶⡠⣊
⣿⣿⣿⣿⣿⣿⣿⢸⣇⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡿⢟⣻⢟⣫⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⡿⣿⢋⣨⣴⣾⡟⡀⢻⣧⢻⣻⣿⣿⡿⣿⣿⣿⣿⣿⣿⣎⣿⣦⠀⠀⢲⣙⣿⣿⣿⠛⠋⠁⠀⠀⣿⣿⣿⣿⣿⡿⢁⡠⠚⠉⣡⢯⣾⣿⣿⣿⣿⡿⢷⣶⢶⠴⣪⣮⣿⣟⣛⣛⠿⠟⠉⣴⢾⣫⣾⣿⣿⣟⣵⣿⣿⣿⣿⢇⣵⠟⢡⢌⢕⣾⣿⣿⣿⣿⣿⡿⣽⡿⣴⣽⣏⣶⣿⣿⣿⣿⣿⣷⣝⠻⠇⠀⠀⠀⠀⠙⠛⠛⠿⠉⣴⡿''', 0.5)
def guard_art():
    echo('''⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣹⡏⣼⢏⣛⣛⢻⣿⣿⡏⠛⢸⣷⡟⡿⢸⠿⣟⣻⣭⣷⣾⣿⣿⣿⣿⣿⣿⠿⣟⣛⣯⣵⣶⣮⣿⣿⣿⣿⣿⣿⡿⠿⣛⣻⣩⣵⣶⢧⣿⣯⣿⢳⠓⠚⠛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣜⢿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⡟⢠⣶⢸⣿⡿⠿⣻⣈⢥⣰⡠⠻⠿⠅⣶⣻⣿⣿⣿⡿⠿⣟⣫⣬⣵⣶⣾⣿⢯⣿⣿⣿⣿⠿⠿⣛⣯⣬⡷⣲⣾⣿⣿⢧⣿⣿⢏⣿⢯⡿⢡⠂⠠⢲⣮⣾⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣭⣿⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⡿⢠⣾⠿⢹⣶⣿⣿⣿⣿⣶⣿⣙⢛⣶⣄⢛⣻⣭⣽⣶⡟⣽⣿⣿⣿⣾⡿⠿⣏⣻⢯⣽⣶⣾⡟⣽⣿⣿⡿⣵⣿⠿⠿⣋⣻⡯⢅⣾⡟⡾⣥⠏⢀⣠⡼⠿⣛⣻⣯⣽⣵⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣛⣻⣭⣽⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣟⣛⣛⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⡟⢁⣴⣾⣿⢸⣿⣿⣿⣿⣿⡯⠿⣳⣿⣿⣿⣸⣻⣿⣿⡿⢞⣛⣫⣭⣿⣆⣾⣿⣿⣟⣾⣿⣿⡟⢾⣛⣛⣏⣭⣥⣮⣿⣟⣿⡿⠕⣾⣿⡿⣽⡟⠀⢀⣶⣷⣿⣿⣿⣿⣿⣿⣿⡿⠿⣛⣛⣻⣭⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣟⣛⣻⣭⣽⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⣛⣛⣭⣽⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⡟⢠⡾⢿⣟⣻⢸⣿⣿⣛⣭⣭⡶⣤⣛⡿⢷⣭⣭⡭⣷⣶⣿⡟⣽⣿⣿⣟⡾⠿⢿⣟⣬⣭⣷⣶⣾⡿⣱⣿⡇⣿⣿⣟⣿⡿⠿⣁⣼⣿⡟⣽⡿⠁⢀⣾⣿⠿⢿⣟⣻⣯⣯⣷⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢿⣛⣻⣭⣭⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣟⣛⣫⣭⣽⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⡞⢪⣶⣿⢏⣿⣿⣿⣿⣿⣿⣿⣿⣟⢿⣿⡻⣿⢮⡻⣵⣿⠿⢿⣚⣻⣭⣽⣶⡞⣿⣿⣿⣟⣼⣿⣿⡿⠳⢟⣛⢱⣿⣿⣿⣿⡇⣿⢳⣿⡟⣼⣿⠃⠉⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣗⣛⣻⣭⣽⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣛⣿⣿⣯⣵⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣟⣛⣿⣭⣭⣷⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢣⡞⢠⡿⢟⣛⣿⣭⣵⣽⣿⣿⣿⣿⣿⣿⣮⣟⡣⠿⣿⣥⣷⣾⣿⣿⡟⣿⣿⣿⣿⣽⠿⢛⣛⣽⣭⣽⣷⣾⣿⢯⣿⣼⣿⡟⣽⣿⣷⣷⣿⡿⣽⣿⠇⢀⣠⣿⣾⣿⣿⣿⣿⣛⣿⣯⣭⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢟⢛⣛⣿⣯⣭⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢛⣛⣿⣭⣯⣽⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣣⠏⢠⡾⣽⣿⣿⣱⣿⡿⢿⣻⣹⣟⣯⣵⣯⣽⣼⣻⠷⡶⡿⣽⡿⠿⣟⣛⡯⣭⣵⣶⡿⣽⣿⣿⣿⣳⣿⣿⣿⡏⠿⢟⢻⣿⡷⣿⣿⢻⢹⡟⣵⣿⠏⢒⣿⣯⣭⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣛⣻⣭⣭⣽⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣟⣛⣿⣭⣭⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣣⠏⠰⠿⣿⣛⣿⣭⣗⣶⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⣶⣾⣿⣿⡿⣽⣿⣿⣿⣻⠿⢿⣟⣋⣯⣭⣷⢆⣾⣿⣿⢾⣿⣿⠟⣿⢸⢸⣸⣿⠏⣂⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣭⣽⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣛⣿⣯⣭⣵⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣯⣽⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⠏⣠⣾⣿⢯⣿⣿⡿⣾⡿⢇⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣏⣽⡿⠿⣛⣙⣯⣭⡵⣶⣾⣿⡿⣣⣿⣿⣿⢿⠿⠟⣛⣋⢾⣿⡟⣾⡏⢿⡜⠿⢫⣾⣿⣟⣛⣛⣯⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣛⣟⣯⣭⣵⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣱⠃⣴⠿⢿⣋⣻⣭⣽⣶⢢⣿⣿⣿⣯⣿⣿⣿⣿⣿⣷⣮⣥⣝⣛⢳⣶⣿⣟⣽⣿⣿⣿⣾⠿⣟⣛⣽⡭⣭⣿⣶⢟⣵⣿⣿⡿⣾⣫⣿⣿⣧⡅⣿⣶⣮⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣭⣭⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣯⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣛⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣵⠃⣰⣾⣿⣿⡿⣻⣿⣿⠯⠿⣿⣋⣽⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⠧⠿⣿⣛⣫⣭⣽⣶⣾⣫⣿⣿⣿⢿⡾⢟⣻⣥⣽⣿⣿⡿⢃⣿⣿⣿⣿⣇⢇⣿⣷⣿⣿⣷⣮⡻⢿⣛⣯⣭⣭⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣟⣛⣿⣿⣭⣵⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⠃⣴⡿⢿⣟⣛⣻⣭⣵⣲⣾⣿⣿⡿⣻⣿⣻⣿⣿⣿⣛⡻⠛⢋⣵⣿⣿⣿⡿⣵⣿⣿⠿⢵⣛⣛⣿⢭⣼⣿⣿⣿⣿⣿⣿⣿⠟⣼⣿⣿⣿⣿⣿⠼⢻⡿⡽⣯⢟⣿⣻⣷⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢯⣉⣹⣿⣿⣿⢿⣿⣏
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢋⠜⠁⣴⣶⣿⣿⣿⣿⣿⠟⡵⣟⣻⣧⢍⣵⣾⣿⣿⣿⣿⣿⣿⣿⠯⢿⣿⣛⣻⣭⣽⢿⣶⣿⣿⢟⣿⡿⣳⣿⣿⣿⣿⣿⣿⣿⣿⡿⢡⣿⣿⣿⣿⣿⣿⡇⣌⣹⣧⣝⠆⢯⣼⣯⣿⣷⣝⣿⣿⣭⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⠿⢟⣾⣿⣿⣿⣿⣿⣿⣿⡿⣛⣿⡯⠭⠭⣿⣟⣫⣞⣭⣭⣭⣵⣶⣶⣾⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡱⡣⠠⠾⣿⣛⣯⣭⣷⣶⣿⣟⣽⣿⣿⣫⡿⢿⣿⣿⣿⣿⣿⢟⢉⣵⣿⡿⣣⣿⣿⣿⣷⣿⠿⠿⣛⡛⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢨⣿⣿⣿⣿⣿⣿⡇⣇⣿⣋⣈⠰⠼⢽⣿⣾⣿⣿⣿⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡭⣷⣶⣶⣿⠿⠯⢽⣷⣛⣛⣫⣭⣷⣾⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⢿⣿⣻⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⠞⢁⣴⣿⣿⣵⣿⡿⠿⠿⣛⣋⣼⣯⣽⣶⢎⣾⡿⡿⣛⣿⣭⡴⡴⠿⢿⣛⣙⣿⣭⣵⣶⡾⣿⣿⡿⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣟⡷⣹⣟⠒⣿⢱⣻⣿⣏⠜⢚⣷⣰⣻⡿⣻⣿⣯⢻⣿⣯⣭⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⣿⣿⣿⣿⣿⣦⣾⣿⣿⣭⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⡿⢿⣟⣛⣛⢿⣯⣭⣷⣶⣶⣦⣝⠿⠾⠳⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡵⠁⣐⣛⣻⣭⡼⣷⣶⡿⣳⣿⣿⢯⣾⣿⠿⢵⢟⣛⣛⣭⢭⣿⣾⣾⣫⣿⣿⣿⣯⣾⣿⣿⢯⡾⠿⢟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⣿⣿⣿⣿⣷⣿⣿⣧⠠⢬⣽⡎⡀⣘⠿⠯⢛⣴⣧⣿⣿⣿⣷⡿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⣟⣛⡛⣿⣭⣭⣿⣷⣶⣾⣿⣿⣿⣷⣽⣿⣯⡅⢿⣿⣿⣿⣿⣿⣿⣶⣾⣷⡈⣯⡻⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢣⠎⣢⣾⣯⣿⣿⣯⠾⠿⣟⣚⣫⣭⣽⣖⣶⣾⣿⣫⣾⣿⡿⣳⣿⣿⡿⠵⢿⣟⣛⣥⡭⣽⣶⣶⡾⡿⡫⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⡇⡙⢤⡱⠯⣨⣿⣥⣿⣿⣿⣷⣯⢽⣿⣜⢿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⢿⣟⣛⢋⣭⣭⣽⣷⣶⣾⣿⣿⣿⣿⣟⣛⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣼⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⠔⢁⣐⣿⡭⣽⣷⣶⣧⣿⣿⣟⣽⣿⣿⣻⠿⠿⢟⣛⣛⣿⣭⣽⣯⣶⣾⡿⣫⣿⣿⡿⣻⡿⠿⢿⣋⣚⡜⣿⣿⣿⣿⣿⣿⣙⣽⣿⣿⣿⣿⣿⣿⣿⠻⣿⣿⣿⣿⣿⣿⣿⣛⣿⠈⠁⠩⣋⣾⣿⣽⢟⣿⣿⣿⣿⣿⣿⢿⣿⣿⣎⣿⠿⠿⢿⣟⣛⣻⣿⣿⣯⣹⣶⣶⣾⣿⣿⣿⣿⠿⠿⠟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣸⣿⣿⣿⣿⣿⣿⣿⣿⣏⠁⣷⡼⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡡⠋⣠⣿⣿⣟⣿⠿⢿⡽⣛⣛⣯⣭⣽⣷⣶⣿⣿⣿⣿⣿⣿⣿⠟⢵⣟⡛⣋⣭⣭⣭⡿⣖⣪⣔⣴⣿⡿⢍⣼⣿⣿⢟⣯⡿⢟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⡇⣐⠽⣛⢯⣫⣾⣿⣿⣭⣛⣿⣿⣽⣿⣿⣿⣷⣻⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⡿⣳⡟⡝⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠀⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠣⠎⢀⣬⣭⣽⣷⣶⣶⣿⣿⣿⣿⡿⠿⠿⠿⣏⣻⣯⣭⣭⣿⣷⢦⣶⣿⣿⣯⣾⣿⣟⡯⡴⠾⣿⣟⣟⣭⡭⣵⢿⣽⣿⣵⣿⠫⣢⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡷⣀⢢⠝⢫⣤⢿⣿⣷⣿⣾⣿⣾⡼⣿⡿⣿⣿⣷⢻⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⢟⣽⣟⣞⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡃⣿⣿⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠫⠐⢠⣴⡿⠿⠿⣟⣛⣻⣻⣥⣿⣷⣶⣾⡿⣫⣿⣿⣿⣿⡿⠿⠟⣷⣛⣛⣛⣭⣯⣷⣶⣾⣿⣿⣿⣿⣿⣿⢿⣷⡿⣿⠟⡝⣾⢫⢾⣿⣿⣿⡿⣳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡂⢿⠞⠘⣗⡕⡐⣿⣛⢿⣿⣟⣲⡾⣿⡻⣿⣿⣿⣿⣷⢻⣾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣾⣿⢟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡫⠈⢀⣴⣶⣾⣿⣿⣿⣿⣿⡷⠿⢟⣟⣛⣛⣻⣬⣭⣭⣥⣶⣿⣿⣿⣿⣿⣿⣿⡿⠿⢿⣟⣛⣻⣿⣯⣭⣭⣽⢦⣿⡟⢑⡑⣼⣸⣿⣗⣿⣿⣿⣿⣾⣾⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣟⣿⣹⣷⢹⠁⡖⠈⢿⣞⣩⣿⡻⣯⡹⣫⡻⢿⣻⣻⣾⣿⣿⣿⣧⢻⣯⣿⣿⣿⣿⣿⣿⣿⢯⣿⢟⢪⣿⣿⣿⣿⣿⣿⣿⣉⣉⣉⣴⡶⠤⠭⠍⠁⣶⣶⣾⡍⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡫⠪⠢⠶⣿⣛⣟⣯⣭⣭⣽⣶⣶⣾⣿⣿⣿⣿⣿⠿⠿⢿⣿⣛⣻⣿⣭⣭⣽⣿⣶⣶⠰⢷⢿⣿⣿⣿⣿⣿⣿⣿⢯⣿⢟⣵⣏⡜⣡⣿⢏⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢸⣤⣷⡬⠋⢻⣯⡭⣧⣿⣟⣡⣿⣫⡿⣹⣽⢿⣿⣿⣿⣯⢿⣷⡽⣿⣿⣿⣿⣳⣿⢯⣢⣿⣿⣿⣿⡏⣿⣿⣿⣿⠰⣴⣶⣶⠀⢸⣿⣿⢸⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⣸⣾⡿⠿⠿⣿⣿⣿⣛⡛⣛⡛⣫⣭⣿⣷⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣸⣿⣿⣿⣿⣿⣿⣏⣾⣯⣿⣿⠏⣼⣿⡯⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣣⢾⢸⣯⢒⢹⡜⠰⡮⣾⠬⢻⢷⠚⣛⢞⢣⣉⢾⠮⢾⣿⣿⣿⡞⣿⣿⣾⣿⣿⢸⣿⡳⣳⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⢀⣻⣿⣟⣩⣼⡟⠍⢾⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣷⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣭⣶⣿⣿⣿⣿⣿⣿⣿⣿⢸⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣾⣿⣿⣿⡏⣼⣿⢃⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣿⢸⣿⠑⡑⣿⣓⣲⣅⠅⡛⡨⠟⢁⢑⣏⠶⣙⠟⣿⣿⣿⣿⣷⢹⣿⣿⣿⣿⡿⡳⣵⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⠸⣿⣶⣾⠀⢸⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢛⣏⢡⣿⣿⣿⣿⣷⣽⡟⡏⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠀⢭⢺⣿⡥⣪⢜⢿⣷⣝⠞⡶⣴⣾⣤⣭⣻⢒⣳⣎⣿⣽⣿⣿⣿⣷⣮⢹⣿⣿⣕⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⡄⢺⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣎⠤⠤⣴⣛⢶⡆⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⢺⡟⣾⣿⣿⣿⣿⣿⣿⢸⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣇⠁⣾⣿⠹⡬⡴⡩⢣⡶⠿⣎⣜⢿⣽⣿⣿⣇⣉⣻⣿⣾⣿⣿⣿⣿⢹⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⠿⡿⠿⢟⡸⠿⠟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⠀⢿⡿⠿⣸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⢻⣿⣿⣿⣿⣿⣿⡏⡟⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡞⣆⣿⡿⠈⡇⡝⡛⢿⡿⢶⣟⠽⢗⡿⢛⢿⣵⣻⢛⣛⣿⣿⣿⣿⣿⣾⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣿⣤⣬⡍⢡⣴⣶⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢺⣿⣿⠈⣯⣾⣿⢹⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣀⣘⣿⣛⣻⣧⣥⣭⡍⣥⣼⣭⣽⣭⣭⣿⣿⣿⣭⣽⣯⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⣟⠏⡷⠺⣡⣿⡼⣏⣭⡼⣧⣄⢯⣿⣼⣿⣛⣻⣻⣿⡿⣿⣿⣿⣿⣧⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢸⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⠀⣿⣿⣿⢸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣾⣿⣿⣿⡿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢿⣿⣷⣾⣿⣿⣿⣷⣾⣿⣷⣶⣷⣶⣲⣶⣶⣶⣥⣭⣩⣭⣽⣓⢺⡿⣄⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠻⠿⠿⠷⠸⠿⠿⠹⠿⣿⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣺⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣺⣿⣿⣿⣿⢸⣿⣿⣤⣿⣿⣟⣼⡇⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⢸⢹⣟⣿⣷⣹⣿⡇⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣞⣿⣿⣿⣿⣿⣿⣭⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣟⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣸⣿⣿⠁⣿⣿⣿⢸⡇⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⢸⢸⣿⣷⣷⡽⣿⡇⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⡇⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⠘⠟⠿⢀⣻⣿⣻⡸⠇⣿⣿⣿⣿⣿⣯⣍⠻⢼⣿⣿⣿⣿⣿⠈⠏⠿⠿⠸⠿⠽⠇⠇⢿⠿⢿⣿⣿⣿⡿⠿⡿⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⡇⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣾⣿⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣟⢲⣄⠻⢿⣿⡏⠀⠀⠀⢰⣾⣦⠀⣢⡀⣄⢸⣌⢲⠀⠀⠐⠶⠶⣶⣶⠶⠌⠛⠓⠀⠀⡈⠉⣍⢉⣉⣉⣉⣀⠉⢡⠭⢼⠿⠯⠿⣟⣛⣛⣛⣛⠛⠛⡻⢿⢟⣿⣿⣿⢿⠿⠿⠿⠿⠿⠿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡸⠿⡟⣿⣿⣿⣿⣿⣿⣟⣇⣹⢿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢸⣿⣷⣧⡋⠁⠄⠀⡀⡾⣿⣿⣇⢿⣇⡟⢸⣿⣜⣇⠀⠀⠰⢶⠠⣨⡍⣳⡆⠀⠀⡼⠀⠠⣽⢸⣷⣿⣿⣿⠀⠘⣆⠀⠀⢀⣉⡙⢻⡟⣭⡙⠛⠀⢀⣿⣼⣿⣿⣿⣿⣿⣾⣿⣿⣇⡠⢦⠀⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣵⣷⠙⠿⠿⠿⠿⣿⣶⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣿⠃⢱⠀⠀⡇⣇⢸⣿⣿⡸⣏⣷⡘⣿⣿⣮⠓⢄⣀⠶⠿⠿⠿⠯⠀⣠⡼⠃⢠⢱⣏⣾⣿⣿⣿⢻⡇⠀⠹⣆⠃⣉⣉⣓⣾⣿⣿⣧⠀⣠⣾⣷⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⡆⣄⣊⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣿⣷⢉⣷⣷⠉⣭⣭⣤⣤⣤⣤⣌⣉⣉⣉⣉
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⢿⡿⠀⡌⠂⢀⡁⣿⢸⣿⣿⡇⡯⣿⠁⣿⣿⣿⣿⡆⣭⣭⣿⣻⣿⣉⣈⢁⣄⣾⡏⣼⣿⣽⣿⣿⢯⣿⡇⣾⣇⣬⣥⡒⠾⠿⠿⠽⠏⢗⣫⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣿⠀⡀⠜⡵⠀⠹⣾⣿⣟⡫⣭⣭⣭⣭⣍⢹⣿⣿⣿⣯⣭⣭⣭⣿⣶⣶⣶⣼⣿⣿⣿⣷⣲⣶⣴⣶⣶⣶⣶⣾⡿⣧⡏⣿⣾⣮⢷⡝⣿⣿⣿⠿⠿⠿⠿⠿⠿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢘⡛⣛⣙⣛⣛⣻⣿⣿⣿⣿⣿⣥⣗⣲⣤⣤⣤⣤⣧⣤⣵⣿⣯⢩⡅⠀⡀⣷⠃⠁⣿⡞⣿⣿⢱⡿⢻⡆⣿⣿⣿⣿⣧⣞⢿⣿⣿⣿⣿⣿⢸⡟⣿⣇⡿⣿⡇⣿⣯⣿⣿⣷⢸⣿⣿⣿⣿⣇⣿⣾⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡏⠈⡂⢴⠣⡇⠀⠛⣻⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣥⡿⡃⣿⣿⣿⣤⢻⣬⡻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⠃⡐⢀⢻⣧⠀⣿⣧⣿⣿⠘⣷⠘⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡇⣿⣯⣇⡹⣥⡿⢊⣿⣿⣟⠈⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢧⣹⠇⠅⡃⢸⢌⣸⡀⠂⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣱⢇⣷⣿⣿⣿⢰⢹⣿⣏⢿⣿⣿⣿⣿⣟
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡇⣿⣿⣿⣿⣿⣿⣿⣿⣟⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⢀⢀⢠⠀⢻⠆⠸⣿⡸⣿⡄⣿⢱⡄⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⠂⣧⢘⢿⣿⣿⣿⡻⣟⡰⣾⣿⡇⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣾⣟⠀⢖⠀⡞⠈⢕⡇⠀⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⣽⣶⣶⣶⣯⣟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡾⣣⣿⣿⣿⣿⡏⣸⢸⢋⡹⢷⣿⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⠟⣛⡻⣷⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠈⡐⠠⠁⡜⣥⢀⢿⡇⣿⡇⣿⠣⡁⣿⣿⣿⣿⣿⢾⣿⣿⣿⣿⡼⣿⢀⡷⢈⣾⣿⣿⣿⣿⣬⣟⣨⣽⡿⣸⡟⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⡉⠀⠃⡌⣶⢨⢼⡸⡈⠒⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣣⣿⠟⢋⣭⣭⢭⣟⢿⣿⣜⢿⣿⣿⣿⣿⣿⣿⠋⣿⣿⣿⣿⣿⣿⡿⣿⣏⡇⡇⢠⣾⣷⣝⣧⡭⣭⣭
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⠧⣰⣿⣿⡞⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢀⠐⠀⠉⠀⢻⡄⠘⣷⢹⡅⢿⡇⠁⣿⢿⣿⣿⣿⣸⣿⣿⣿⣿⣷⣺⢾⢧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡇⡇⣿⣹⡿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢗⡒⠏⠁⡄⡴⢠⢰⠸⢸⢱⣷⠸⢆⢻⣿⣿⣿⣿⣿⣿⣿⣿⢧⣿⢏⣰⣿⣿⢿⢸⣿⣷⣹⣿⡞⣿⣿⣿⣽⡿⣡⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⡇⢱⣿⣿⣿⣿⣿⣿⣯⣻
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣧⣿⣿⣿⣿⣿⣿⠀⣭⡏⣿⣭⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠢⠈⠄⡁⢠⠘⣇⠡⠹⢸⣧⣾⡇⠆⡀⠀⢹⣿⠋⠠⣿⣿⡟⣭⡙⣾⢸⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡃⡞⡿⢇⢿⣿⡿⠿⢿⣿⣿⠟⢿⣿⣿⣿⣿⣿⡼⣼⠏⢸⢀⠅⠑⢚⡬⣇⢿⠰⡇⠈⣎⢿⣿⣿⣿⣿⣿⣿⣿⣾⣿⠀⣭⣮⣽⣱⢪⣶⣶⣸⣿⣧⢸⣿⣿⣿⣾⡟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⡿⣫⣿⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡏⣿⣿⣿⣿⣿⣿⠀⠿⠿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢘⠠⡁⠢⠈⠤⡁⠿⠀⢇⢻⣿⢹⡇⠀⣿⣶⣟⣻⣷⢠⣿⣿⣧⣛⢧⣿⣼⢳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢀⡸⡿⣸⣿⣁⠀⣸⣿⣷⣀⣸⣿⣿⣿⣿⣷⢻⠟⠸⢡⢊⢆⢶⡞⣽⢹⡸⡇⢹⡄⣶⡎⣿⣿⣿⣿⣿⣿⣿⣸⣿⠀⣿⣿⣿⣻⢸⣿⣿⡇⢸⡇⣻⠟⠿⠟⢋⣾⣿⣿⣿⣿⣿⡿⢻⣿⣿⣿⠿⢺⣿⣿⡿⣋⣼⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡯⣿⣿⣿⣿⣿⣿⠀⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⢽⠐⠌⠀⡁⢂⠑⢀⠐⡎⡸⣿⢸⣧⠀⢈⣻⡃⠀⢱⡌⠨⠏⢫⣿⢼⢿⣽⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢼⣿⡞⣿⠟⢻⣿⡿⠛⢿⣿⡿⠛⣿⣿⡟⡜⣸⢀⢃⢯⢻⠸⣈⣧⢹⣐⣷⢸⡅⣷⡀⣾⡜⣿⣿⣿⣿⣿⣿⣿⣿⠀⣶⣴⣚⢲⢒⣂⣒⡂⢟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣯⣿⣿⣿⣿⣿⣿⠀⣛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⢦⠀⢌⠲⠌⠡⠈⠠⠈⡇⠀⣿⡿⣯⣰⣿⣿⣷⣶⣾⢵⣄⣠⡞⣿⡼⣾⢿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⡇⣇⠹⢣⣿⣇⣀⣼⣿⣄⣰⣯⣿⡽⢃⠡⢢⣻⣸⡇⡘⢁⢎⢈⢿⡸⡇⣿⡌⣧⠚⠷⠸⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⡿⢹⣿⣿⡇⠏⢿⣿⣿⣿⣿⣿⣿⣿⠿⠝⠿⣿⣿⣿⣿⣯⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡟⣿⣿⣿⣿⣿⣿⡀⠿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⡄⡣⡍⠢⡑⢠⠒⡰⠂⡁⢺⠀⠸⡟⣿⡇⠉⠀⢹⣿⠛⠙⢿⣿⠷⠛⠇⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡯⢸⣻⣳⣟⣟⡯⢴⣶⣿⡿⢿⣿⣵⣿⣿⠁⠈⠈⠸⡇⢹⢠⠄⠇⠎⡞⡜⣧⠹⡎⣷⡙⣷⡎⣟⠸⣿⣿⣿⣿⣿⣿⠑⣒⣚⣙⢷⢮⣉⡉⠅⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣄⠘⢿⣿⣿⣿⣷⡆⢰⣿⣿⣿⣿⣿⣿⣿⣟
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⡐⢆⢵⣄⠰⠈⠂⡁⠄⠡⠌⠘⡃⠠⠁⣇⡇⣘⣦⣾⣿⣤⢀⣴⢮⡀⠀⡀⣸⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⢜⠀⠐⢻⣽⡁⠁⣽⣿⡀⣠⣿⣿⢯⡿⢁⠀⣾⢡⢻⢸⡏⣧⠂⡆⢗⠡⡸⠇⣿⡌⣷⠹⣖⠸⢗⡸⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⢸⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣏⢿⣜⢷⡌⢿⣿⣿⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠠⡉⢦⠚⡳⣷⠄⠀⠄⠡⠄⠠⠀⠀⠂⢦⠸⣧⣿⢻⡿⠿⢽⢱⣿⢸⣝⣿⡇⣿⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡵⣞⣦⣴⢿⣿⣷⣿⣿⣿⣿⣯⣿⣿⡟⣠⠃⢸⡇⡜⡙⣃⣷⣰⢠⠇⡍⣆⢿⣽⣯⢿⡏⣇⡻⣌⢸⣷⡹⣿⣿⣬⣿⣤⣭⣭⣽⣯⣜⣛⣛⣣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⣿⡎⡿⢸⣿⣿⢿⡇⣼⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⡙⢦⡱⢍⡺⡢⠔⠠⢐⠠⡀⠀⠆⡰⠸⣧⢻⣽⣿⣇⠀⢰⣷⢰⣦⢺⣿⡇⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⡻⣟⡻⣿⠿⠉⢹⣿⣿⣯⠢⢀⡤⠂⣻⢁⢣⣧⡏⢽⢛⣸⢸⢹⡟⣘⢯⣸⠇⣻⠙⣧⢻⡜⠿⢥⡹⣷⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡼⣿⡄⢸⣿⣿⠘⣼⣿⣿⣿⣿⣿⠛⠛⠛⠁
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠂⡕⠢⣛⠖⢝⠈⠂⠈⠀⠀⡂⠀⠁⢈⢠⣿⣷⣹⣿⣿⣷⢹⣿⣧⢩⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡟⣿⣧⣊⣡⣿⣧⣤⣾⢟⣿⠃⣠⠟⢠⡁⡟⢨⢣⡇⡗⡟⡟⡟⣌⣿⢱⡟⣌⣧⣸⣏⣻⡟⣾⠳⡼⠌⢇⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣸⣿⣿⣸⣿⣿⣿⢹⣿⢣⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢀⠁⠲⣌⠓⢻⡙⠂⢁⡂⢀⠀⠀⠂⠀⠀⠐⢼⣟⣿⣷⡹⣿⣿⣸⣿⣿⣼⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣻⣿⣿⣿⣿⣿⣿⣧⣿⡻⠐⡡⠊⡤⡅⢳⠺⡊⠁⢡⣥⢫⠟⡞⢯⡑⡑⠈⢪⠡⡻⣏⢷⡙⣶⢻⡴⡜⣦⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⢧⣿⢇⣛⣛⣛⣛⣛
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢀⡁⠐⢄⣁⠢⠬⢅⠀⢍⠲⢄⡐⠠⡈⣠⣾⣿⢿⠸⣿⣿⣯⣻⢼⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣽⠡⢎⢰⢃⣰⠶⠈⣿⢳⡛⡞⣂⠇⠃⢂⢽⣏⠨⠊⢃⠄⢣⡼⠇⣹⡏⣼⢃⣽⡄⣣⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⢳⣿⣿⣿⣿⣿⠿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠠⢤⡁⠁⠤⢀⠀⡐⠀⢑⠀⢁⠢⠈⣠⣾⣿⠿⣿⡏⢆⣿⣿⢿⡝⣷⣮⣛⠛⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠋⣵⣿⠃⠀⠎⢠⠋⠠⢚⣫⠄⡻⣻⣤⢢⠚⡄⢣⢂⠅⣢⡭⣔⣂⡡⠓⡉⣄⢻⡹⢦⢿⡿⡼⣦⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣏⣧⣤⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠂⠀⢀⢐⠀⡂⠀⠈⠐⠈⠄⠀⣡⣾⣿⣿⢯⣾⣿⣿⢸⣯⢿⣯⣷⣝⣟⠿⣿⣦⣄⡀⠘⠿⡿⣿⣿⣿⣿⣿⣿⣿⡿⡿⠿⢿⡿⠉⠉⢁⣀⡄⠠⣰⣿⣿⠇⠊⡁⠜⡠⠃⡰⢋⡵⢫⢵⣨⠸⢟⠏⠎⠁⠀⠪⣝⠩⠛⢛⢫⠿⢭⣞⢧⡞⣮⡶⠱⡵⡌⠅⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⡀⠒⠢⠄⠉⠉⠈⠉⠀⠀⠀⢀⣶⣿⣿⣿⣧⣾⣿⣿⣿⣮⣿⣾⣿⡿⣟⢿⡿⣮⡻⡿⣿⣗⢤⠀⡀⠀⠀⠀⠀⢀⣀⣈⣀⣡⠕⣠⣴⡾⣫⠟⡘⣶⠿⠛⠁⢁⠔⡁⠞⢱⠋⡤⠊⡤⠡⠎⠵⣣⢆⠄⠀⣤⠸⢳⢆⡌⡠⣥⢙⢺⣿⡽⠙⢱⠜⢀⢈⠀⠚⡀⠢⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢠⣌⢉⠁⠀⠀⢰⣷⡋⠀⠀⠀⢿⢿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣷⢻⣿⣷⡝⣷⣯⢻⣷⠙⣧⣿⣮⠷⣄⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣵⠟⠼⠋⡄⠀⢀⠀⠈⠰⡁⠂⢠⠎⡐⢀⡰⣁⠄⡼⢐⠉⡆⡠⠀⢠⡂⠸⠃⣗⢸⢼⡗⡏⡻⢟⡶⣤⣡⢶⣦⣱⣚⣄⢀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣭⣭⣿⣿⣟⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣛⡉⠉⣣⡽⡯⠀⣤⣪⣁⠀⠀⢀⣿⣿⠁⠀⠀⣘⣟⣾⡿⣿⣿⣿⣿⣿⣿⣿⣼⣿⣶⡻⣯⣿⣯⣿⣯⣻⣷⡙⣿⣿⣟⣿⣷⡄⠄⠀⠀⠀⣠⣾⣿⣿⢿⠟⡉⢀⢀⢱⠃⢰⣷⣴⣇⠀⢣⠂⢁⠞⡡⢀⡑⣉⡎⢡⠃⠈⠀⠃⠀⣿⢢⡍⣀⠕⡿⢰⡇⡇⢹⢠⠉⠙⢿⣷⣯⣝⠳⣶⣦⡀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⣭⣿⣿⣿⣿⣻⣿⣿⢛⣵⣾⠿⢃⣼⣫⡾⠡⢲⠟⠍⠀⡀⠀⣼⣿⣿⣀⠀⠀⢻⣿⣼⣏⣜⣿⣿⣿⣷⣿⣿⣿⣿⣿⢏⣿⣿⣿⣿⣷⣿⣻⣟⢈⣿⢿⣿⡻⣿⣦⠁⣤⣾⣿⣿⣿⣟⣴⣏⣡⡸⠠⠀⡎⠈⠏⠈⠏⠉⢁⠬⢠⡔⡡⢒⡑⢉⡬⠁⠞⠡⠆⡘⢰⣿⠖⠠⡂⡤⠀⠼⢰⡇⡛⢸⠀⣏⢢⠊⠻⣿⣷⣦⣍⠹⣎⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣭⣤⣬⡍⣿⣿⣿⣿⣯⠏⢶⣾⣿⣿⡿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢟⣿⡾⡻⢑⣡⣿⡿⠋⠀⠀⠀⠀⠀⠋⣽⡀⣿⣿⣿⣿⣤⢶⠸⣿⣿⣮⣎⢬⣟⢿⣿⣿⣻⣿⣿⣴⣿⣿⢿⣿⡟⢷⣝⣿⣿⡭⢻⣷⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⠹⠋⠆⠂⡠⢁⠔⠀⠠⠠⡠⢜⡐⣂⠄⢈⡲⠉⠐⢀⠔⢀⠎⠠⠊⡰⠂⣸⣏⣸⢏⣲⢧⡾⢡⡎⢠⠅⡽⢠⠆⠹⠈⡄⡠⠙⢿⣿⢿⣮⣈⠟⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣡⣿⣿⣿⣿⣿⢰⣹⠿⠛⡁⠈⠅⡛
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡋⢠⣾⣿⣿⣾⣧⣾⡿⠋⠀⠀⠀⠀⣀⣠⡄⣀⣿⣦⣾⣿⣿⣿⣿⣿⡇⢻⣿⣿⣿⢮⢿⣿⣿⣿⣿⣽⢻⣿⢷⣶⣾⣿⡽⣽⣷⣮⣻⡷⢟⠻⣿⣯⣿⣿⣿⢹⣿⡿⡿⠁⠀⠀⣀⠉⡔⡘⡰⠐⣘⢅⣻⣭⣶⡘⣥⠜⠴⠋⡴⠊⡈⠁⡒⢁⠄⢁⠀⣿⣤⡂⣼⣋⣞⣅⡞⠐⢋⠸⣥⣾⣗⣊⣠⣥⣭⣭⣷⣙⣻⡿⢻⣍⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣿⣿⣿⣿⣿⣿⢒⣺⣶⣶⣦⣄⣀⣀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢫⡎⣶⢿⢟⣾⣿⣿⡵⠢⣾⣇⣀⡀⣴⣾⣿⣿⣿⣿⣷⣿⣿⣿⣿⣟⣿⣿⣿⡌⣿⣼⢿⣎⢧⢢⣎⣿⣽⢿⢹⣿⣷⡽⢻⡿⣿⣧⡻⣿⣿⣿⠿⠻⣿⡸⣿⣿⣿⠛⠋⠀⠀⠀⡀⣤⠏⡐⡒⠀⢠⠠⢰⡷⠾⢭⣽⡳⢀⣤⢠⣤⢁⡈⠀⠈⠀⠚⠠⢣⣦⠉⠛⠿⢶⣶⣭⣟⡻⠿⠿⢷⡶⣭⣭⣿⡿⢿⣿⣭⡻⢿⣶⣶⢻⣿⡿⢜⠛⢗⡮⣝⢿⣿⣿⣿⣿⣿⣿⣿⣿⡔⣿⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⡿⣶⣫⣾⢿⡐⣟⣫⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⢹⣷⢾⣳⣽⢮⣿⣿⣆⡉⣿⣧⡻⢷⣙⣮⠻⣮⢸⣿⢿⢇⠗⢛⠉⠘⢿⡐⢈⢁⠀⠠⡠⡠⠈⡜⠞⡜⣱⣷⠿⢽⣶⣟⣡⢳⣱⣏⢶⠣⣳⣾⣿⢦⣷⢦⢾⣇⠻⣿⣿⣿⣿⣷⣶⣦⣭⣝⣛⣛⣒⣻⣶⣤⣄⣀⡀⠀⠈⠉⠒⠤⠵⠼⠺⢿⣿⣿⣾⣦⣑⣷⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢉⢴⣽⣿⢗⣽⣾⣿⣵⡍⣽⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣟⡙⣿⣿⣯⠿⠟⢉⣴⣿⣟⢿⣿⡿⣷⣿⣽⡏⣿⢹⣯⣷⣬⢿⣝⠜⡮⡁⠐⠾⠀⡄⠈⠀⠠⢤⡄⠈⠉⣁⣙⡁⡁⢿⣩⡜⣠⠥⣹⣹⣷⠃⠤⢦⣷⣿⣯⣢⣷⣿⣾⠟⣿⡵⡫⣽⣯⣭⠬⠙⣿⣿⣿⣿⣿⡿⡿⣟⡛⣻⠭⠙⢒⣒⣂⡂⣉⡉⣉⣍⢁⡉⣍⢉⢷⣛⡙⡙⠿⠿⣟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠛⠛⠻⣿⢓
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣡⡆⣼⣿⢟⣭⣿⣿⣿⣿⣿⣿⡽⣿⣿⣿⣿⣿⣿⡿⣟⣭⣽⠿⠿⣿⣟⡿⡿⠿⣛⣉⣥⣤⣶⣿⣿⣿⢻⣿⣷⣿⣇⣿⣿⣷⣿⣿⣯⣷⢿⡷⡁⢩⠃⠙⠀⠀⡀⣄⢰⣸⡜⡀⣈⠁⡄⠃⠠⣉⡓⠓⠶⣦⣭⡍⡔⢀⢋⡕⢔⢦⢦⣿⣍⣬⢿⡿⣵⣞⣽⡿⠱⠛⠉⣬⣠⣶⣿⠿⣛⣯⠽⠐⢉⣡⣥⣤⣷⣿⢲⠃⣈⢉⡷⠧⢁⣿⣿⡾⣧⢿⣼⡞⣯⣿⣿⣽⣿⣿⣿⣭⣟⡷⣽⡿⣿⣿⡙⣿⣿⣿⣿⣿⣿⣷⣿⠧⠂⠀⠀⠈⢄
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢫⣾⠿⣣⣩⣶⣿⣿⣿⣿⣿⣿⣿⣿⣓⡰⠿⠟⠉⠁⠀⢀⡀⣄⣤⣴⣴⣶⣶⣶⣷⣿⣿⣿⣿⣿⣿⣿⣿⣯⢿⡿⣿⣿⣿⣷⡿⣿⣞⢿⡎⢻⣷⢄⡰⠐⠀⢀⣠⣵⣻⡽⣿⢻⣱⡹⠘⠇⠃⠞⠷⣖⣉⣇⠗⠾⣄⣬⣱⣻⣮⣭⣪⠾⠿⠽⣟⣫⣿⠿⠃⣨⠷⣪⣵⣶⠿⢟⠽⢗⣊⣭⣶⣶⣿⣿⡟⡟⣿⣿⣿⣏⠀⠐⡙⠏⠗⢰⣾⣼⣿⣿⣻⡞⣇⢧⣿⣹⣿⣿⣸⣿⣟⢿⣿⢻⣧⠯⠑⢯⣑⢿⣿⣿⣿⣿⣿⣿⣿⣯⠧⠀⠀⢼⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⡿⢟⢫⣾⣿⣧⠹⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⢀⣀⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡝⣿⣭⣿⣿⡟⣿⣿⡿⢷⡍⣶⡉⠁⠀⣀⠐⢷⢛⢧⣃⣻⣿⡿⠳⢹⣿⡞⣲⣷⡾⣦⣋⣛⡿⢶⣦⣽⢯⣽⣿⣻⣻⣿⡜⠛⣘⣉⡤⣖⣥⣴⢿⣻⠽⢞⣫⣷⣿⣿⣿⣿⣟⣿⣿⢿⣿⣽⣹⣿⣿⣿⣴⡄⡑⠰⡀⣻⣿⣇⣿⣿⡿⣿⣿⣾⣿⣟⣿⣿⣇⣿⣿⣾⣿⡾⡇⠙⢻⣷⡌⣗⢍⣻⣿⣿⣿⢿⢿⣿⠀⠀⠀⣼⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣫⣥⣶⢫⣾⣿⣿⡷⢹⣿⠟⠉⠀⢀⣲⢮⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣯⢹⣽⣿⣎⢿⣷⠣⡞⠬⢁⣴⡆⢀⢠⠋⠐⣬⣥⢫⠻⡆⠠⠸⣯⠀⡅⣯⣿⡿⣯⡿⣿⢻⣺⡋⣩⣷⢸⠧⠟⢩⣶⣶⣿⣿⣿⣯⡧⣛⣋⠱⣾⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⡼⣿⣿⡟⣿⢿⣿⣯⣿⣮⣾⣹⣿⣿⣹⣻⣿⣷⣿⣾⣇⣷⣿⢻⣿⣿⣿⣿⣷⣿⠀⢀⠴⠨⢻⣿⣸⣇⣿⣮⡻⣿⣴⣾⣶⢦⣗⣁⣈⣉
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣱⣿⡾⣿⡿⣲⣿⣿⢿⠋⠁⠈⠠⣠⣤⣾⡟⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⢿⡿⡘⡿⠀⣠⡴⢘⡿⡌⢉⡓⠛⢓⢉⢉⣆⡸⡁⠇⢘⠉⠀⠅⣾⡯⣿⠿⡿⣿⣾⣟⣵⠃⠘⠤⢈⣯⣾⣿⣿⣿⡿⣋⠁⠲⡽⠿⡧⠼⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣧⣿⣿⣷⢿⣿⣿⣿⣧⣏⣿⡟⡿⠿⠿⣇⢿⢿⠿⠿⢿⡿⣼⣟⣿⣿⣿⣿⣿⣿⢠⡘⠃⢁⣥⣳⢹⣿⢸⡻⣿⢮⡻⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⣋⣴⡿⢟⡾⡫⣢⣿⣿⢕⠅⠀⣤⣴⣿⣿⡿⣣⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣼⣟⠿⠁⢄⣚⣃⡀⠀⠁⡁⡘⢻⣛⣈⡇⣴⠿⣧⢳⡆⠘⡎⠀⠀⠬⣝⡟⣻⣿⢷⠀⣣⣵⢒⢯⣼⣿⣿⣟⢷⣫⣵⣾⢏⠠⣷⠽⠇⢹⡿⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡿⢟⢻⣿⣳⣤⣤⠿⣷⣾⣖⣒⣓⣛⣳⣶⣶⡶⢭⣅⣉⡙⠛⢿⣿⣿⣷⣷⣿⣿⣿⡾⣿⣿⣟⣻⣼⣿⣜⠿⠿⠿⡿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡍⣿⡟⢑⢕⣠⢽⣿⣿⠋⢀⢀⣾⣿⣿⡿⢫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣷⣾⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⣩⠀⡡⣽⢼⣿⣿⣦⣐⢄⢄⢪⣛⡍⡀⡇⢿⡻⣾⡇⠀⢠⠤⡄⣵⡏⡟⠹⣛⣤⣾⣯⣥⣶⣿⣿⡿⠨⣡⣿⣿⢻⣟⢸⣄⢿⣤⡠⣄⡅⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢛⣑⣶⣶⢶⣛⣿⣭⣭⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣭⣽⣒⢆⣉⠛⠿⣿⣻⣿⣿⣧⣿⣿⢻⣿⣧⣿⣿⣷⡠⣦⣂⡟⡍
⣿⣿⣿⣿⣿⣿⣿⣿⡎⢸⣿⣭⣴⡿⠋⠁⣢⣅⣾⣿⣿⠏⣱⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣮⣿⣿⠟⢡⢔⣵⣿⣿⣦⣬⡹⣿⣿⣥⡷⣻⣿⣿⣿⡿⣫⡼⢣⣷⠅⢾⣾⣿⣾⣻⣦⣎⠙⢚⣿⠁⢢⢄⢻⡇⣿⢥⠀⠶⢄⢇⢟⢐⣤⣾⣿⣿⣿⣿⣿⡿⣿⡅⢸⣴⡇⣿⣿⡞⣿⡎⣿⣵⣢⣾⣿⣽⣿⣿⣿⣿⣿⡿⣛⢍⡡⠴⣚⣯⣵⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣵⡢⣌⠙⠿⣿⣿⣽⣿⣿⣿⢿⣿⣿⣿⣿⣜⢿⣷⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⢉⡍⣤⡆⣾⣿⣿⣿⡿⢏⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠊⣚⣵⣿⣿⣿⣿⣿⡿⣛⠀⣿⣿⡿⣲⣿⡿⣋⡚⡋⢀⣾⣿⡇⡘⣿⣿⢿⣿⣿⡇⢶⠲⣦⠀⡌⣈⣯⣼⣷⠂⠖⡘⢛⣩⡶⣿⣿⣿⣿⡿⣻⠽⢫⣾⣿⣧⠹⣿⢹⡽⣿⣯⣿⣿⣹⣿⣿⣾⣿⣿⣿⡿⢿⣻⣦⢿⣻⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⠄⠀⠩⡿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣧⣻⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣶⡏⠳⣿⣷⣿⣿⣿⠿⠊⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⡇⣿⣿⣿⣿⣿⣧⣿⡏⢠⣺⣿⣿⣿⣿⣷⣝⣷⡿⠀⣼⡿⡋⢟⣯⡘⢫⣾⠇⠘⢧⠸⣿⣧⣿⢃⣿⠟⣸⠦⠙⠼⠃⢷⢠⣖⡏⣾⣣⡇⢈⣴⣟⣩⣾⣿⣿⣿⡿⢻⢵⣿⣬⣼⣿⣿⡇⢿⡼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢞⣻⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠘⠿⣿⣿⣿⣸⣿⣿⣿⣿⣿⡍
⣿⣿⣿⣿⣿⣿⣿⣿⠇⣼⣿⢇⣐⠉⡟⣿⣿⡯⠕⣼⣿⣿⣿⣿⣿⣿⢟⣯⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⡿⢪⢿⣯⣿⣿⣿⣿⣿⡟⠔⢠⣿⣻⣷⢟⣭⣶⣿⣣⣦⣦⡈⣧⢿⣿⢟⣾⠃⠶⠋⣢⣺⣿⣅⢐⠏⢯⢸⢩⢇⣴⣿⣿⣿⣿⡿⣿⡿⣫⣷⢿⣶⣿⣿⣿⣿⣿⣧⡜⣧⢿⣿⣿⣿⣿⣿⣿⣿⠿⣟⣧⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡃⡄⢻⣿⢿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⡏⡞⣻⡏⢸⣿⣧⠡⣻⣿⣣⣰⣿⣿⣿⡿⣿⣿⢇⣾⣿⣯⣿⣿⣿⣿⣿⣿⣿⣮⣾⣿⡮⡊⢿⡿⣿⠿⠟⠉⢀⣴⣿⣷⠟⠅⣯⠹⣿⣿⣿⣿⣿⣃⣦⠈⡃⠛⠁⠀⠒⠐⠲⠦⠴⠶⣰⣏⡇⣣⣴⣿⣿⣿⣿⠿⣿⢿⣻⣾⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣭⢻⡾⣿⣿⡿⣛⡵⣊⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠂⠄⠑⠻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⢘⢠⣿⢇⣾⣿⣻⡗⡙⣾⡻⣿⣿⣿⣿⣿⣿⣫⣾⣿⣿⣿⣿⣣⣿⢻⣯⣿⣿⣿⣿⣿⣿⣪⣤⣁⢀⡠⠶⢲⠟⣻⢟⣳⣷⣖⣙⣛⡿⢿⣿⡿⢏⣾⣿⣶⠟⣡⣬⠈⣐⠣⠍⠠⠥⠬⠯⣪⣾⢟⣿⣿⣿⣻⣿⣿⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡜⣷⢿⡫⢏⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡩⢀⠡⠹⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⢩⡿⣿⣽⣿⠟⣿⣇⣿⡌⢿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⠗⣊⣙⣙⣻⠿⣿⣿⣿⣟⣽⣿⣟⣿⣿⣿⢏⣿⠻⣫⣾⣿⣿⣿⡿⣷⡩⣵⣿⣿⢟⡐⣲⣢⡐⢃⠉⢸⣯⣈⣹⣵⣿⡿⣷⣿⣿⣿⣿⣟⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⣡⠙⡘⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠁⢻⣷⣿⣿⣿⢾⣿⡟⣿⣯⡞⢍⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢠⢿⣿⣍⣙⢿⣗⠜⣻⣿⣿⣿⣿⢉⣿⣶⣶⣶⣎⣰⣿⣿⡿⣿⣿⣿⣿⡇⣿⢟⣑⣫⣭⣵⡿⡶⡰⡶⠶⢦⣼⣿⣿⣫⢞⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣎⢴⡉⢏⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⢠⢏⣽⣿⣿⣧⣳⣿⣧⣿⣿⣗⣎⣫⣬⣿⣻⣿⣿⣿⣿⣿⣟⣒⣳⣻⣟⣻⣿⣿⢿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣽⣵⣿⣿⣿⣿⣿⣿⣿⢱⣟⣛⣭⣿⣿⣿⡄⣵⡡⣠⣿⣿⣯⣾⣳⣿⣿⡿⣫⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⣷⡉⢝⣿⣿⣿''', 0.5)
#--------------------------------------------



def witch_riddle():
    global player_name
    global witches_secret
    witch_hut_art()
    echo("\x1B[3m"+"* Beyond the mist, you finally see something other than muggy foilage and sullen trees.\n"+"\x1B[0m",0.07)
    echo("\x1B[3m"+"* As you get closer, the figure looms, pointing in all directions, uninviting.\n"+"\x1B[0m",0.07)
    time.sleep(0.4)
    echo("\x1B[3m"+"* Creaks and stomps increase in volume, you prepare to be greeted by whatever monster awaits in the hut..\n\n"+"\x1B[0m",0.09)
    echo("\x1B[3m"+"* A beast, a cracken, a witch, the anticipation grows with each step.  \n\n"+"\x1B[0m",0.09)
    echo("* Don't be fooled, {}.\n\n".format(player_name),0.2)
    echo("\x1B[3m"+"STOMP...\n"+"\x1B[0m",0.09)
    echo("\x1B[3m"+"STOMP...\n"+"\x1B[0m",0.09)
    print("\033[1m"+"Witch:"+"\033[0m")
    witch_art()
    echo("IIIIIYYAAAAAA GIRLIEEE!!! ~~",0.001)
    echo("MA NAMES VALERIEE~~\n",0.001)
    echo("\x1B[3m"+"...\n"+"\x1B[0m",0.09)
    print("\033[1m"+"Valerie..?:"+"\033[0m")
    echo("how ya doin?",0.09)
    echo("I was waitin for you. When I heard ya was in town I was GASSED!!! You wouldn't BELIEVE IT.\n",0.019)
    echo("\x1B[3m"+"You're...pleasantly surprised..\n"+"\x1B[0m",0.07)
    print("\033[1m"+"Valerie:"+"\033[0m")
    echo("I got somethin for you. I got a lil secret for ya. But i'm on a busy schedule here!! I got my knickers making business to tend to babes, and you don't...",0.019)
    echo("\x1B[3m"+"...\n"+"\x1B[0m",0.09)
    echo("look like a customer...\n",0.09)
    echo("BUT I COULD BE WRONG!!! Anyways..READ THIS AND HURRY UP ON OUT!!\n",0.019)
    echo("\x1B[3m"+"She tosses a scroll at you, with...sparkles?.. Anyways.\n"+"\x1B[0m",0.07)
    print('''
    ╔═════════════════════════════════════════════════════════════════╗
    ║    Truly no one is outstanding without me, nor fortunate;  ✧    ║
    ║  ✧ I embrace all those whose hearts ask for me.      ✧      ✧   ║
    ║    He who goes without me goes about in the company of death;   ║
    ║  ✧ and he who bears me will remain lucky for ever.              ║
    ║    But I stand lower than earth and higher than heaven.     ✧   ║
    ╚═════════════════════════════════════════════════════════════════╝''')
    print("\033[1m"+"Valerie:"+"\033[0m")
    echo('''
    Is it:
    A) Wisdom
    B) Happiness
    C) Humility
    D) Patience\n''',0.019)
    
    while True:
        answer = input("").lower()

        if answer == "a":
            echo("INCORRECT!!!!!!!!",0.001)
        elif answer == "b":
            echo("INCORRECT!!!!!!!!",0.001)
        elif answer == "d":
            echo("INCORRECT!!!!!!!!",0.001)
        elif answer == "c":
            echo("WOOOOOOOOWWWW... GIRLIE!!!!!!! Correct!!!\n",0.001)
            witches_secret += 1
            break
        else:
            echo("Cm'on A, B, C or D.\n",0.019)

    print("\033[1m"+"Valerie:"+"\033[0m")
    echo("Well...You got that one right!!!!....",0.019)
    echo("NOW GET OUT OF ME SWAMP!!!!!!!!!!!!!!!!!!!\n",0.001)
    echo("\x1B[3m"+"* She slams the door, and you turn back to the boat, more confused than before....\n\n"+"\x1B[0m",0.09)
    return carriage()



def game_intro():
    global player_name
    global player_class
    echo('Jake, Keanu, Danya and eve', med)
    time.sleep(3)
    print('')
    echo('╔═══════════════════════════════════════════╗', fast)
    echo('║░░░░░▒▒▒▒▒▓▓▓▓▓ S L A Y E R ▓▓▓▓▓▒▒▒▒▒░░░░░║', slow)
    echo('╚═══════════════════════════════════════════╝', fast)
    time.sleep(1)
    print('')
    echo_dialogue('Guard: Halt! Who goes there?')
    guard_art()
    player_name = input('[State your name:] ')
    echo_dialogue(f'Guard: Ah, greetings {player_name}!')
    while True:
        echo('╔═══════════════ OPTIONS: ═══════════════╗', fast)
        echo('║ 1. Who are you?                        ║', fast)
        echo('║ 2. What is this place?                 ║', fast)
        echo('║ 3. What is there to do around here?    ║', fast)
        echo('╚════════════════════════════════════════╝', fast)
        choice = input('[Choose an option:] ')
        if(choice == '1'):
            echo_dialogue(f'{player_name}: Who are you?')
            echo_dialogue('Guard: I\'m the town guard!')
            echo_dialogue('Guard: It\'s my job to keep out any unwanted visitors from Farmouth,')
            echo_dialogue('Guard: Be they human or otherwise.')
            echo_dialogue(f'{player_name}: ...or otherwise?')
            echo_dialogue('Guard: Yep! There are a lot of nasty beasts and monsters out there!')
        elif(choice == '2'):
            echo_dialogue(f'{player_name}: What is this place?')
            echo_dialogue('Guard: Farmouth is just our humble little town, quite a ways out of the way.')
            echo_dialogue('Guard: We\'re surrounded by forest, caves, a swamp, and the mountain range.')
            echo_dialogue(f'{player_name}: It seems like a nice little place.')
            echo_dialogue('Guard: Oh yes, it\'s normally peace and quiet around here,')
            echo_dialogue('Guard: but in recent times we\'ve been having some... trouble.')
        elif(choice == '3'):
            echo_dialogue(f'{player_name}: What is there to do around here?')
            break
        else:
            echo('Please enter a choice number (1-3).', fast)
    echo_dialogue('Guard: Glad you asked!')
    echo_dialogue('Guard: Recently, there have been disturbing reports of sightings in the surrounding areas.')
    echo_dialogue(f'{player_name}: What sort of sightings?')
    echo_dialogue('Guard: Oh, the usual things - angry giant rats, ferocious bears... a few dragons...')
    echo_dialogue(f'{player_name}: Hmm... I think I can help you with that!')
    echo_dialogue('Guard: Really What exactly are you?')
    time.sleep(1)
    echo('╔════════════════ CLASS: ════════════════╗', fast)
    echo('║ 1. Mage                                ║', fast)
    echo('║ 2. Archer                              ║', fast)
    echo('║ 3. Warrior                             ║', fast)
    echo('║ 4. Paladin                             ║', fast)
    echo('╚════════════════════════════════════════╝', fast)
    echo('* Tip: There is no "correct" choice - pick whatever you want to be!', fast)
    while True:
        choice = input('[Choose a class:] ')
        if(choice == '1' or 'mage' in choice):
            player_class = 0
            echo_dialogue(f'{player_name}: I\'m a Mage.')
            break
        elif(choice == '2' or 'archer' in choice):
            player_class = 1
            echo_dialogue(f'{player_name}: I\'m an Archer.')
            break
        elif(choice == '3' or 'warrior' in choice):
            player_class = 2
            echo_dialogue(f'{player_name}: I\'m a Warrior.')
            break
        elif(choice == '4' or 'paladin' in choice):
            player_class = 3
            echo_dialogue(f'{player_name}: I\'m a Paladin.')
            break
        else:
            echo('Please enter a number (1-4).', fast)
    echo_dialogue('Guard: Aha, just the sort of person we need!')
    echo_dialogue('Guard: You can go on and head into town and take a look around, if you like.')
    echo_dialogue('Guard: When you want to head out and start exploring, just speak to the carriage driver.')
    echo_dialogue(f'{player_name}: I shall, thank you sir!')
    time.sleep(1)
    echo( f"* ...Our hardy adventurer {player_name} approaches Farmouth Village,", med)
    echo( "* A small noble village out in a valley of the Hykalude Mountains,", med)
    echo( "* Called to the village by the promise of work, gold, and wonders.", med)
    time.sleep(2)
    echo( "* This is where your journey begins.", med )
    time.sleep(2)



game_intro()

next_location = village_start()
while next_location != None:
     next_location = next_location()

print('Thanks for playing!')
time.sleep(2)
print('')
print('Credits:')
print('Jake - Game Design, Programming, Art')
print('Keanu - Game Design, Programming, Art')
print('Danya - Game Design, Programming, Art')
print('eve - Game Design, Programming, Art')
time.sleep(2)
print('')
print('Special thanks to:')
print('codenation.com')
print('python.org')
print('stackoverflow.com')
print('github.com')
print('repl.it')
print('and all the other people who helped us along the way!')
time.sleep(2)
print('')
print('This game was made for the 2020 PyWeek 30 game jam.')
print('The theme was "The Last".')
print('The game was made in 7 days.')
time.sleep(2)
print('')
print('The game is licensed under the MIT License.')
