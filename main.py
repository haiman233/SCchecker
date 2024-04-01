#coding=utf-8

import os
import yaml

from time import time

_VERSION = '1.2 SHOT'
MAXINT = 2147483647
CRTs = "ENHANCED_CRAFTING_TABLE, MAGIC_WORKBENCH, ARMOR_FORGE, COMPRESSOR, PRESSURE_CHAMBER, SMELTERY, ORE_CRUSHER, GRIND_STONE, ANCIENT_ALTAR, NONE".split(', ')
BIOMES = set("BADLANDS  BAMBOO_JUNGLE  BASALT_DELTAS  BEACH  BIRCH_FOREST  CHERRY_GROVE  COLD_OCEAN  CRIMSON_FOREST  CUSTOM DARK_FOREST  DEEP_COLD_OCEAN  DEEP_DARK  DEEP_FROZEN_OCEAN  DEEP_LUKEWARM_OCEAN  DEEP_OCEAN  DESERT  DRIPSTONE_CAVES  END_BARRENS  END_HIGHLANDS  END_MIDLANDS  ERODED_BADLANDS  FLOWER_FOREST  FOREST  FROZEN_OCEAN  FROZEN_PEAKS  FROZEN_RIVER  GROVE  ICE_SPIKES  JAGGED_PEAKS  JUNGLE  LUKEWARM_OCEAN  LUSH_CAVES  MANGROVE_SWAMP  MEADOW  MUSHROOM_FIELDS  NETHER_WASTES  OCEAN  OLD_GROWTH_BIRCH_FOREST  OLD_GROWTH_PINE_TAIGA  OLD_GROWTH_SPRUCE_TAIGA  PLAINS  RIVER  SAVANNA  SAVANNA_PLATEAU  SMALL_END_ISLANDS  SNOWY_BEACH  SNOWY_PLAINS  SNOWY_SLOPES  SNOWY_TAIGA  SOUL_SAND_VALLEY  SPARSE_JUNGLE  STONY_PEAKS  STONY_SHORE  SUNFLOWER_PLAINS  SWAMP  TAIGA  THE_END  THE_VOID  WARM_OCEAN  WARPED_FOREST  WINDSWEPT_FOREST  WINDSWEPT_GRAVELLY_HILLS  WINDSWEPT_HILLS  WINDSWEPT_SAVANNA  WOODED_BADLANDS".split(' '))

saveditems = set()
parentsCategories = set()
normalCategories = set()
items = set()
totalBug = 0
totalWarn = 0


class color:
    # Text color                          Background color
    black = '\33[30m'                   ; bblack = '\33[40m'
    red = '\33[31m'                     ; bred = '\33[41m'
    green = '\33[32m'                   ; bgreen = '\33[42m'
    gold = '\33[33m'                    ; bgold = '\33[43m'
    blue = '\33[34m'                    ; bblue = '\33[44m'
    purple = '\33[35m'                  ; bpurple = '\33[45m'
    cyan = '\33[36m'                    ; bcyan = '\33[46m'
    lightgray = lightgrey = '\33[37m'   ; blightgray = blightgrey = '\33[47m'
    gray = grey = '\33[38m'             ; bgray = bgrey = '\33[48m'
    white = reset = '\33[39m'           ; bwhite = '\33[49m'


def error(string, end='\n'):
    if totalBug < config['MaxPrintBug']:
        print(f'{color.red}{string}{color.reset}', end=end)


def warn(string, end='\n'):
    print(f'{color.gold}{string}{color.reset}', end=end)


def report(i, Warn=False):
    global config, totalBug, totalWarn, MaxBug, MaxWarn
    if Warn and totalWarn == MaxWarn:
        totalWarn += 1
        error(f"[Warn]{totalWarn}. 在 {i}:", end="\n  ")
        error(f"[Warn] Warn打印数量已达到上限！")
    elif Warn and totalWarn < MaxWarn:
        totalWarn += 1
        warn(f"[WARN]{totalWarn}. 在 {i}:", end="\n  ")
    elif totalBug == MaxBug:
        totalBug += 1
        error(f"[BUG]{totalBug}. 在 {i}:", end="\n  ")
        error(f"[BUG] Bug数量已达到上限！请修复以上Bug再运行本程序！")
    elif totalBug < MaxBug:
        totalBug += 1
        error(f"[BUG]{totalBug}. 在 {i}:", end="\n  ")


def printc(string):
    print(f'{color.blue}{string}')


def startWith(string, target):
    if string[:len(target)] == target:
        return True
    return False


def getYamlContext(file):
    try:
        result = yaml.load(file, Loader=yaml.FullLoader)
        if result is None:
            return {}
        return result
    except FileNotFoundError:
        error(f'{file}未找到')
        return {}
    except PermissionError:
        error('无权限')
        return {}


def RewriteSlimefunItems():
    global config
    if config['SlimefunItemsPath'] == 'default':
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..\\Slimefun\\Items.yml")
    else:
        file_path = config['SlimefunItemsPath']
    with open(file_path, 'r', encoding='utf-8') as file:
        regNames = getYamlContext(file).keys()
    with open('__SlimefunItems.yml', 'w', encoding='utf-8') as file:
        yaml.dump({'items': list(regNames)}, file, allow_unicode=True, encoding='utf-8')


def getSaveditems():
    items = set()
    for root, dirs, files in os.walk("saveditems"):
        for file_name in files:
            if file_name.endswith(".yml"):
                file_name = os.path.basename(file_name)
                items.add(file_name[:-4])
    return items


def getSlimefunItems():
    with open('__SlimefunItems.yml', 'r', encoding='utf-8') as file:
        sfItems = getYamlContext(file)
    return sfItems['items']


def getVanillaItems():
    with open('__VanillaItems.yml', 'r', encoding='utf-8') as file:
        mcItems = getYamlContext(file)
    return mcItems['items']


def inSlimefun(item):
    intersection = SlimefunItems.intersection(set([item]))
    if len(intersection) == 0:
        return False
    return True


def inVanilla(item):
    intersection = VanillaItems.intersection(set([item.upper()]))
    if len(intersection) == 0:
        return False
    return True


def inSaveditems(item):
    intersection = saveditems.intersection(set([item]))
    if len(intersection) == 0:
        return False
    return True


def inBiome(item):
    intersection = BIOMES.intersection(set([item]))
    if len(intersection) == 0:
        return False
    return True


def isVanilla(item, position):
    if not startWith(item, "SKULL") and not inVanilla(item):
        report(position)
        error(f"{item} 可能不是正确的原版物品！")


def isSlimefun(item, position):
    if not inSlimefun(item) and item not in items:
        report(position)
        error(f"{item} 可能不是正确的粘液物品！")


def isSaveditem(item, position):
    if not inSaveditems(str(item)):
        report(position)
        error(f"{item} 可能不是正确的保存物品")


def isBiome(item, position):
    if not inBiome(item):
        report(position)
        error(f"{item} 可能不是正确的群系")


def isCategory(category, position):
    if (not startWith(category, "existing:") and category not in normalCategories):
        report(position)
        error(f"{category} 可能不是有效的正常分类！")


def isItemTypeProper(data, position):
    dType = data['item-type']
    dId = data['item-id']
    if dType == "CUSTOM":
        isVanilla(dId, position+'item-id ')
    elif dType == "SAVEDITEM":
        isSaveditem(dId, position+'item-id ')
    else:
        report(position+'item-type')
        error(f"{dType} 可能不是一个有效的类型")


def isInt(num, position, bottom=0, top=MAXINT, Warn=False):
    if isinstance(num, int):
        if not bottom <= num <= top:
            if Warn:
                report(position, Warn)
                warn(f"{num} 不在区间[{bottom},{top}]内（不影响运行）")
            else:
                report(position)
                error(f"{num} 不在区间[{bottom},{top}]内")
    else:
        report(position)
        error(f"{num} 不是整数")


def getItemMaxStack(item):
    return MaxStacks[item]


def isAmountProper(item, dAm, position, zero=False, warn=False):
    stack = getItemMaxStack(item) if inVanilla(str(item)) else 64
    isInt(dAm, f'{position}', 0 if (stack == 0 or zero) else 1, stack, warn)


def TIA(dat, position, zero=False, warn=False):
    dType = dat['type']
    dId = dat.get('id', 'N/A')
    dAm = dat.get('amount', 1)
    if dType == 'SLIMEFUN':
        isSlimefun(dId, position+'id ')
    elif dType == 'VANILLA':
        isVanilla(dId, position+'id ')
    elif dType == 'SAVEDITEM':
        isSaveditem(dId, position+'id ')
    elif dType == 'NONE':
        ...
    else:
        report(position+'type')
        error('type 只能是 VANILLA, SLIMEFUN, SAVEDITEM, NONE 中的任意一个！')
    if dType != 'NONE':
        isAmountProper(str(dId).upper(), dAm, position+'amount', zero, warn)


def isRecipeProper(data, position):
    crt = data['crafting-recipe-type']
    if crt not in CRTs:
        error(f'{crt} 可能不是正确的配方类型')
    temp = []
    recipe = data['crafting-recipe']
    for j in recipe:
        dat = recipe[j]
        dType = dat['type']
        dId = dat.get('id', 'N/A')
        dAm = dat.get('amount', 1)
        TIA(dat, position+f'crafting-recipe 的 第 {j} 个物品 的 ')
        temp.append([dType, dId, dAm])
    idx = 1
    if crt in {'ENHANCED_CRAFTING_TABLE', 'MAGIC_WORKBENCH', 'ARMOR_FORGE', 'PRESSURE_CHAMBER'}:
        for k in temp:
            if k[2] != 1:
                report(position+f'crafting-recipe 的 第 {idx} 个物品')
                error('amount 必须为 1')
                break
            idx += 1
    elif crt in {'COMPRESSOR', 'PRESSURE_CHAMBER', 'ORE_CRUSHER', 'GRIND_STONE'}:
        for k in temp[1:]:
            if k[0] != 'NONE':
                report(position+f'crafting-recipe 的 第 {k} 个物品')
                error(f"第{k}槽必须为NONE类型")
                break
            idx += 1
    elif crt == "ANCIENT_ALTAR":
        for k in temp:
            if k[0] == 'NONE':
                report(position+f'crafting-recipe 的 第 {idx} 个物品的 type')
                error(f"第{idx}槽必须不为NONE类型")
                break
            if k[2] != 1:
                report(position+f'crafting-recipe 的 第 {idx} 个物品的 type')
                error(f"第{idx}槽的 amount 必须为 1")
                break
            idx += 1
    elif crt == "SMELTERY":
        sum_dict = {}
        for k in temp:
            if k[0] == 'NONE':
                continue
            key = k[1]
            value = k[2]
            if key in sum_dict:
                sum_dict[key] += value
                if sum_dict[key] > 64:
                    report(position+f'第 {idx} 个物品的 amount')
                    error("单种物品消耗数量不能超过64！")
                    break
            else:
                sum_dict[key] = value
            idx += 1


def isRunningRecipeProper(data, position):
    recipes = data['recipes']
    for j in recipes:
        try: 
            int(j)
        except TypeError:
            report(position+'recipes')
            error(f"{j} 不是有效的配方编号")
        recipe = recipes[j]
        speed = recipe['speed-in-seconds']
        isInt(speed, position+f'第 {j} 个配方的 speed-in-seconds')
        Input = recipe['input']
        Output = recipe['output']
        if len(Input) != 2:
            report(position+f'第 {j} 个配方的 input')
            error('input参数数量错误')
        if (Input['1']['id'] == Input['2']['id']):
            report(position+f'第 {j} 个配方的 input')
            error('两槽位物品相同，这会导致一些bug！')
        if (Input['1']['type'] == 'NONE' and Input['2']['type'] != 'NONE'):
            report(position+f'第 {j} 个配方的 input')
            error('你不能设置第1格无物品，但第2格有物品！')
        if (Output['1']['type'] == 'NONE' and Output['2']['type'] != 'NONE'):
            report(position+f'第 {j} 个配方的 output')
            error('你不能设置第1格无物品，但第2格有物品！')
        for k in Input:
            TIA(Input[k], position+f'第 {j} 个配方的 input 的第 {k} 个物品的 ', True)
        if len(Output) != 2:
            report(position+f'第 {j} 个配方的 output')
            error('output参数数量错误')
        for k in Output:
            TIA(Output[k], position+f'第 {j} 个配方的 output 的第 {k} 个物品的 ', True)


def isRunningRecipeProperInGenerators(data, position):
    recipes = data['recipes']
    for j in recipes:
        recipe = recipes[j]
        speed = recipe['time-in-seconds']
        isInt(speed, 'time-in-seconds')
        Input = recipe['input']
        Output = recipe['output']
        TIA(Input, position+'input 的 ', True)
        TIA(Output, position+'output 的 ', True)


def checkScAddon():
    for f in files['ScAddon']:
        printc(f'Testing sc-addon: {f}')
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)
        if 'depend' not in k:
            report(f'sc-addon: {f}')
            error('缺少 depend 参数')


def checkCategories():
    for f in files['Categories']:
        printc(f'Testing categories：{f}')
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)
        for i in k:
            data = k[i]
            item = data['category-item']
            isVanilla(item, i)
            dType = data['type']
            if dType in ('sub', 'seasonal', 'normal', 'locked'):
                normalCategories.add(i)
            if dType == 'nested':
                parentsCategories.add(i)
            elif dType == 'sub':
                dParent = data['parent']
                if not startWith(dParent, "existing:"):
                    if dParent not in parentsCategories:
                        report(f'categories: {f}: {i}')
                        error(f"{dParent} 可能不是正确的父分类！")
            elif dType == 'seasonal':
                dMonth = data['month']
                isInt(dMonth, f'categories: {f}: {i} 的 month', 1, 12)
            elif dType == 'normal':
                # Nothing to do
                ...
            elif dType == 'locked':
                # Nothing to do
                ...
            if 'tier' in data:
                dTier = data['tier']
                isInt(dTier, f'categories: {f}: {i} 的 tier')


def checkMobDrops():
    for f in files['MobDrops']:
        printc(f'Testing mob-drops: {f}')
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)

        for i in k:
            data = k[i]
            dCategory = data['category']
            isCategory(dCategory, f'mob-drops: {f}: {i} 的 category')
            isItemTypeProper(data, f'mob-drops: {f}: {i} 的 ')
            dAm = data['item-amount']
            isAmountProper('__PLACEHOLDER', dAm, f'mob-drops: {f}: {i} 的 item-amount')
            dChance = data['chance']
            isInt(dChance, f'mob-drops: {f}: {i} 的 chance', 0, 100)
            dMob = data['mob']
            if dMob not in entities:
                report(f'mob-drops: {f}: {i} 的 mob')
                error(f"{dMob} 可能不是正确的生物")
            dDisplay = data['recipe-display-item']
            isVanilla(dDisplay, f'mob-drops: {f}: {i} 的 recipe-display-item')
            items.add(i)


def checkGeoResources():
    for f in files['GeoResources']:
        printc(f'Testing geo-resources: {f}')
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)

        for i in k:
            data = k[i]
            dCategory = data['category']
            isCategory(dCategory, f'geo-resouces: {f}: {i} 的 catrgory')
            isItemTypeProper(data, f'geo-resouces: {f}: {i} 的 ')
            dDev = data['max-deviation']
            isInt(dDev, f'geo-resouces: {f}: {i} 的 max-deviation', 1)
            ok = False
            if 'biome' in data:
                ok = True
                dBi = data['biome']
                for m in dBi:
                    isBiome(m, f'geo-resouces: {f}: {i} 的 biome')
                    isInt(dBi[m], f'geo-resouces: {f}: {i} 的 biome 的 {m}')
            if 'environment' in data:
                ok = True
                dEnv = data['environment']
                for m in dEnv:
                    if m not in ("NORMAL", "NETHER", "THE_END"):
                        report(f'geo-resouces: {f}: {i} 的 environment')
                        error(f"{m} 不是正确的类型")
                    isInt(dEnv[m], f'geo-resouces: {f}: {i} 的 environment 的 {m}')
            if not ok:
                report(f'geo-resources: {f}: {i}')
                error(f"未找到 biome 或 environment")
            items.add(i)


def checkItems():
    for f in files['Items']:
        printc(f"Testing items: {f}")
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)

        for i in k:
            data = k[i]
            dCategory = data['category']
            isCategory(dCategory, f'items: {f}: {i} 的 category')
            isItemTypeProper(data, f'items: {f}: {i} 的 ')
            dAm = data['item-amount']
            isAmountProper(data['item-id'], dAm, f'items: {f}: {i} 的 item-amount')
            dPlaceable = data['placeable']
            if dPlaceable not in {True, False}:
                report(f'items: {f}: {i} 的 placeable')
                error(f"placeable 只能为 true 或 false")
            isRecipeProper(data, f'items: {f}: {i} 的 ')
            items.add(i)


def checkCapacitors():
    for f in files['Capacitors']:
        printc(f'Testing capacitors: {f}')
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)

        for i in k:
            data = k[i]
            dCategory = data['category']
            isCategory(dCategory, f'capacitors: {f}: {i} 的 category')
            dType = data['block-type']
            dAm = data['item-amount']
            if dType not in ('DEFAULT', 'default'):
                isVanilla(dType, f'capacitors: {f}: {i} 的 block-type')
                isAmountProper(dType, dAm, f'capacitors: {f}: {i} 的 item-amount')
            dCapa = data['capacity']
            isInt(dCapa, f'acpacitors: {f}: {i} 的 capacity')
            isRecipeProper(data, f'capacitors: {f}: {i} 的 ')
            items.add(i)


def checkMachines():
    for f in files['Machines']:
        printc(f"Testing machines: {f}")
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)

        for i in k:
            data = k[i]
            dCategory = data['category']
            isCategory(dCategory, f'machines: {f}: {i} 的 category')
            dType = data['block-type']
            isVanilla(dType, f'machines: {f}: {i} 的 block-type')
            dBar = data['progress-bar-item']
            isVanilla(dBar, f'machines: {f}: {i} 的 progress-bar-item')
            dStats = data['stats']
            dEC = dStats['energy-consumption']
            isInt(dEC, f'machines: {f}: {i} 的 stats 的 energy-comsumption')
            dEB = dStats['energy-buffer']
            isInt(dEB, f'machines: {f}: {i} 的 stats 的 energy-buffer')
            isRecipeProper(data, f'machines: {f}: {i} 的 ')
            isRunningRecipeProper(data, f'machines: {f}: {i} 的 ')
            items.add(i)


def checkGenerators():
    for f in files['Generators']:
        printc(f"Testing generators: {f}")
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)

        for i in k:
            data = k[i]
            dCategory = data['category']
            isCategory(dCategory, f'generators: {f}: {i} 的 category')
            dType = data['block-type']
            isVanilla(dType, f'generators: {f}: {i} 的 block-type')
            dBar = data['progress-bar-item']
            isVanilla(dBar, f'generators: {f}: {i} 的 progress-bar-item')
            dStats = data['stats']
            dEP = dStats['energy-production']
            isInt(dEP, f'generators: {f}: {i} 的 energy-production')
            dEB = dStats['energy-buffer']
            isInt(dEB, f'generators: {f}: {i} 的 energy-buffer')
            isRecipeProper(data, f'generators: {f}: {i} 的 ')
            isRunningRecipeProperInGenerators(data, f'generators: {f}: {i} 的 ')
            items.add(i)


def checkSolarGenerators():
    for f in files['SolarGenerators']:
        printc(f"Testing solar-generators: {f}")
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)
        for i in k:
            data = k[i]
            dCategory = data['category']
            isCategory(dCategory, f'solar-generators: {f}: {i} 的 category')
            dType = data['block-type']
            isVanilla(dType, f'solar-generators: {f}: {i} 的 block-type')
            dEP = data['stats']['energy-production']
            isInt(dEP['day'], f'solar-generators: {f}: {i} 的 stats 的 energy-production 的 day')
            isInt(dEP['night'], f'solar-generators: {f}: {i} 的 stats 的 energy-production 的 night')
            isRecipeProper(data, f'solar-generators: {f}: {i} 的 ')
            items.add(i)


def checkMaterialGenerators():
    for f in files['MaterialGenerators']:
        printc(f"Testing material-generators: {f}")
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)
        for i in k:
            data = k[i]
            dCategory = data['category']
            isCategory(dCategory, f'material-generators: {f}: {i} 的 category')
            dType = data['block-type']
            isVanilla(dType, f'material-generators: {f}: {i} 的 block-type')
            dStats = data['stats']
            dEC = dStats['energy-consumption']
            isInt(dEC, f'material-generators: {f}: {i} 的 energy-comsumption')
            dEB = dStats['energy-buffer']
            isInt(dEB, f'material-generators: {f}: {i} 的 energy-buffer')
            isRecipeProper(data, f'material-generators: {f}: {i} 的 ')
            output = data['output']
            tickRate = output['tick-rate']
            isInt(tickRate, f'material-generators: {f}: {i} 的 output 的 tick-rate')
            TIA(output, f'material-generators: {f}: {i} 的 output 的 ', warn=True)
            items.add(i)


def checkResearches():
    for f in files['Researches']:
        printc(f"Testing researches: {f}")
        with open(f, 'r', encoding='utf-8') as file:
            k = getYamlContext(file)
        for i in k:
            data = k[i]
            dId = data['id']
            isInt(dId, f'researches: {f}: {i} 的 id')
            dCost = data['cost']
            isInt(dCost, f'researches: {f}: {i} 的 cost')
            for j in data['items']:
                isSlimefun(j, "researches: {f}: {i} 的 items")


def checkAll():
    for i in checkers:
        start = time()
        try:
            i()
        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            error('在获取YAML内容时遇到了错误！')
            error('可能是YAML结构错误！请在下方网站内检查')
            error('https://www.bejson.com/validators/yaml_editor/')
        except KeyError:
            error('未找到参数！')
            error('可能是YAML缺少了参数或参数不完整！')
        print(f'{color.green}Spent {time() - start}s')
    print(f"{color.cyan}Done! {time() - sum_start}s")


try:
    sum_start = time()
    print(f'{color.blue} Loading config')
    with open('SCchecker-config.yml', 'r', encoding='utf-8') as file:
        config = getYamlContext(file)
    if config == {}:
        config = {'MaxPrintBug': 100}
        error("读取config失败！你是否删除了SCchecker-config.yml?")
    ignores = config['ignores']
    files = config['scan-files']
    MaxBug = config['MaxPrintBug']
    MaxWarn = config['MaxPrintWarn']
    checkers = [
        # int just a placeholder
        int if ignores['ignoreScAddon']             else checkScAddon,
        int if ignores['ignoreCategories']          else checkCategories,
        int if ignores['ignoreMobDrops']            else checkMobDrops,
        int if ignores['ignoreGeoResources']        else checkGeoResources,
        int if ignores['ignoreItems']               else checkItems,
        int if ignores['ignoreCapacitors']          else checkCapacitors,
        int if ignores['ignoreMachines']            else checkMachines,
        int if ignores['ignoreGenerators']          else checkGenerators,
        int if ignores['ignoreSolarGenerators']     else checkSolarGenerators,
        int if ignores['ignoreMaterialGenerators']  else checkMaterialGenerators,
        int if ignores['ignoreResearches']          else checkResearches
    ]
    RewriteSlimefunItems()
    SlimefunItems = set(getSlimefunItems())
    loadedItems = getVanillaItems()
    VanillaItems = set((tuple(i.keys())[0] for i in loadedItems))
    keys = []
    values = []
    for item in loadedItems:
        keys.append(tuple(item.keys())[0])
        values.append(tuple(item.values())[0])
    MaxStacks = dict(zip(keys, values))
    saveditems = getSaveditems()
    entities = set()
    for item in VanillaItems:
        if item[-10:] == '_SPAWN_EGG':
            entities.add(item[:-10])
    entities.add("GIANT")
    checkAll()
    print(f'{color.cyan}共{totalBug}个Bug')
    print(f'{color.cyan}共{totalWarn}个Warn')
    print(f'{color.cyan}此脚本实际上并不能找到全部的Bug')
    print(f'{color.cyan}只能尽可能找出潜在的Bug！')
except FileNotFoundError as err:
    error('无法找到文件！')
    error(err)
except BaseException as err:
    error('运行程序时遇到了致命错误，请查看错误信息，确定并非自己的问题后，可联系作者修复！')
    error(err)

"""
'请确保控制台输出的bug（若有）皆已修复，本程序才能正常运行！'
'需要注意的是，此脚本并不会检查任何与name或lore相关的内容！'
'如有误报请联系作者企鹅2793572961'
'此python程序任何人皆可使用，修改，但不得进行任何商业活动、违反公德的行为或违法行为'
'Made by guguguhello'
"""
