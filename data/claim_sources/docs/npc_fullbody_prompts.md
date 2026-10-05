# NPC 半身立绘 → 全身图 生图提示词库（豆包/即梦 + SDXL 通用）

> NPC 3D 管线第 1 步的标准提示词模板（2026-06-23 华夏三 NPC 验证成功的格式）。
> 用法：图生图/参考图模式上传对应立绘 + 提示词；每角色出 2–4 张，选轮廓干净、
> 四肢不粘连的一张进入下一步（去水印 → 混元 3D V3.1 → 50k 面 GLB → NPCModelSetupTool）。
> 新时代 NPC 照此格式续写，勿改动固定句式（比例约束/背景/负向清单）。
> ⚠️ 服饰/鞋履/佩饰必须**严格符合该文明的史实与环境**（先查证角色身份对应的真实装束再下笔，如罗马元老=紫边托加+红色元老靴 calceus、军团兵=环片甲+军靴；勿把同一套默认装束套遍全员）。史实本身即差异化——同一时代全员凉鞋这类同质化是查证不足的症状（2026-07-06 用户反馈）。

## 模板结构（固定句式）

- **英文正向**：`masterpiece, best quality, highly detailed, 1boy/1girl, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, <角色描述>, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style`
- **英文负向**（全角色通用）：`short legs, stubby legs, long torso, disproportionate, chibi, extra arms, extra hands, multiple hands, disembodied hands, mutated hands, extra limbs, extra legs, deformed, bad anatomy, cropped, cut off, out of frame, close-up, bust, multiple people, collage, multiple views, grid, text, watermark, signature, lowres, blurry, cluttered background`
- **中文版**：角色全身描述 + 固定要求句：`要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。`

## 范例存档：华夏 · 守关者（npc_china_guardian，2026-06-23 成功案例）

立绘是红缨兜鍪、黑金重札甲、金兽肩吞、红披风、持长柄大刀的古代将领。下半身补出甲裙+护胫+战靴。

英文正向：
masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Chinese male general guardian warrior, stern face, ornate helmet with a tall red plume, heavy black and gold lamellar armor with red accents, golden beast-head shoulder pauldrons, long flowing red cloak reaching below the knees, armored war skirt, armored greaves, war boots, holding a long-handled polearm with a crescent blade upright in one hand, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

中文版：
一位古代中国男性守关将领/武士的全身立绘。比例自然、约七到八头身、胯在画面中段；面容威严、棕发；头戴带高红缨的华丽兜鍪；身穿黑金相间、缀红的重型札甲，金色兽首肩吞，披及膝以下的红色长披风，下为甲裙、护胫、战靴；一手竖握一柄带弯月刀刃的长柄大刀。（+固定要求句）

---

# 埃及三 NPC（2026-07-04）

## ① 书记官·塞莎（npc_egypt_scribe）

立绘是金星饰发带配白羽、黑发编金辫、金宽项圈、白色无袖长裙配蓝金腰封、薄纱披肩、持纸草卷的古埃及少女书记官。下半身要补出裙摆及地+金色凉鞋。

英文正向：

masterpiece, best quality, highly detailed, 1girl, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 heads tall, hips at the middle of the figure, standing, ancient Egyptian young female scribe, gentle smile, dark tan skin, long black hair with thin golden braids, blunt bangs, golden headband with a blue-gem star ornament and a single white feather, golden tassel hoop earrings, broad golden collar necklace inlaid with lapis-blue stripes, winged-scarab golden pendant with a blue gem, white sleeveless ankle-length dress with golden trim, blue and gold patterned waist sash with a blue-gem round buckle and hanging ornamental bands with golden tassels, golden armlet on the upper arm, golden wide bangles on both wrists, sheer white shawl with golden star patterns draped over the arms, golden sandals, feet visible, holding a rolled papyrus scroll in one hand at her side, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

英文负向：

short legs, stubby legs, long torso, disproportionate, chibi, extra arms, extra hands, multiple hands, disembodied hands, mutated hands, extra limbs, extra legs, deformed, bad anatomy, cropped, cut off, out of frame, close-up, bust, multiple people, collage, multiple views, grid, text, watermark, signature, lowres, blurry, cluttered background

中文版（即梦/豆包）：

一位古埃及少女书记官的全身立绘。比例自然、约七头身、胯在画面中段；深蜜色肌肤、温柔浅笑；黑色长直发间编几缕金色细辫、齐刘海；头戴金色发带，缀蓝宝石八角星饰与一支白色羽毛；金色流苏圆环耳环；金色宽项圈嵌青金石蓝条纹，胸前圣甲虫展翅金坠嵌蓝宝石；身穿白色无袖及地长裙镶金边，蓝金纹样宽腰封嵌蓝宝石圆扣、垂下饰带与金流苏；右上臂金色臂环、双腕金色宽镯；臂间搭白色薄纱披肩绣金色星纹；脚穿金色凉鞋；一手在身侧持一卷纸草。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

## ② 大祭司（npc_egypt_priest）

立绘是光头、额间金印、右眼下荷鲁斯纹、蓝金宽披领、白色层叠长袍、鹰徽腰封、持金色安卡杖的古埃及大祭司。下半身要补出袍摆及地+袍下微露金色凉鞋。

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Egyptian young high priest, calm wise expression, shaved bald head, dark tan skin, golden diamond-shaped mark on the forehead, black eye-of-Horus marking under the right eye, single long golden dangle earring, golden engraved choker, broad blue and gold ceremonial collar inlaid with lapis-blue stripes and a central blue gem pendant, white flowing floor-length layered robe with wide sleeves and golden trim, vertical golden line patterns on the robe, blue and gold waist sash with a central golden winged-falcon emblem, long blue and gold hieroglyph band hanging down the front, golden wide bracelets on both wrists, golden sandals peeking from under the robe, feet visible, holding a tall golden ankh staff upright in one hand, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

英文负向：（同上，通用负向清单）

中文版（即梦/豆包）：

一位古埃及青年大祭司的全身立绘。比例自然、约七到八头身、胯在画面中段；光头、深蜜色肌肤、沉静睿智的神情；额间金色菱形圣印，右眼下荷鲁斯之眼黑色纹样；单侧金色长坠耳环、金色刻纹颈环；肩披蓝金宽礼仪披领（青金石蓝条纹、中央嵌蓝宝石坠）；身穿白色宽袖层叠及地长袍，镶金边、袍面有纵向金线纹样；蓝金腰封中央金色展翅鹰徽，腰前垂蓝底金字圣书体长饰带；双腕金色宽镯；袍摆下微露金色凉鞋；一手竖握一柄金色安卡长杖。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

## ③ 守陵人（npc_egypt_guardian）

立绘是黑金阿努比斯胡狼盔、黑金条纹头巾、赤裸健壮上身配金项圈胸饰、白色缠腰长裙、黑金斗篷、持金色科佩什弯刀的守陵武士。下半身要补出及地缠腰裙+金色护胫+战凉鞋。

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Egyptian tomb guardian warrior, stern face, black and gold Anubis jackal helmet with upright ears and a blue gem on the brow, lower face exposed, black and gold striped headdress draping to the chest with golden tassels, dark tan skin, muscular bare torso, broad golden collar with layered golden chest ornaments inlaid with blue gems, black and gold armlet on the upper arm, golden scaled bracers on both forearms, long white wrapped waist skirt reaching the ankles, black and gold jackal-head belt emblem with a blue gem and diamond-shaped golden pendants, long black cloak with golden patterns behind the shoulders, golden greaves and war sandals, feet visible, holding a large golden khopesh curved sword upright in one hand, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

英文负向：（同上，通用负向清单）

中文版（即梦/豆包）：

一位古埃及守陵武士的全身立绘。比例自然、约七到八头身、胯在画面中段；头戴黑金阿努比斯胡狼盔（双耳竖立、额嵌蓝宝石、露出下半张脸），黑金条纹头巾垂至胸前坠金流苏；深蜜色肌肤、健壮赤裸上身、神情冷峻；金色宽项圈与多层金色胸饰嵌蓝宝石；右上臂黑金臂环，双前臂金色鳞纹护腕；下身白色缠腰长裙及踝，腰间黑金胡狼头徽记嵌蓝宝石、垂菱形金饰；肩后黑色镶金纹长斗篷；小腿金色护胫、脚穿战凉鞋；一手竖握一柄金色弯月形科佩什刀。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

---

# 希腊三 NPC（2026-07-05）

## ① 哲人·苏格（npc_greece_sage）

立绘是橄榄叶冠、白色卷发长须、白色希顿长袍配金色回纹镶边、藏蓝色希玛纯外袍缀金叶纹与金圆胸针的慈祥老哲人。下半身要补出袍摆及地+皮凉鞋。

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Greek elderly philosopher sage, warm gentle smile, wise kind face with wrinkles, curly white hair, long full curly white beard, olive laurel wreath with dark olives on the head, white chiton robe with golden Greek-key meander trim, deep navy-blue himation cloak draped over one shoulder with golden laurel-leaf border patterns, round golden brooch with a flower emblem pinning the cloak at the shoulder, navy sash around the waist, robe reaching the ankles, aged hands gesturing gently, leather sandals, feet visible, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

英文负向：（同上，通用负向清单）

中文版（即梦/豆包）：

一位古希腊老年哲人的全身立绘。比例自然、约七到八头身、胯在画面中段；白色卷发与浓密的白色长卷须、面容慈祥带笑纹；头戴缀深色橄榄果的橄榄叶冠；身穿白色希顿长袍，领口与衣缘为金色回纹（希腊钥匙纹）镶边；斜披一件藏蓝色希玛纯外袍，袍缘绣金色月桂叶纹，肩头以一枚金色花形圆胸针固定；腰间藏蓝腰带；袍摆及踝，脚穿皮制凉鞋；双手自然做出温和的交谈手势。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

## ② 史家·希罗（npc_greece_historian）

立绘是金色月桂细冠、深棕乱发短须、白色短袖束腰袍配金边、藏蓝披巾绣金纹、棕色皮革斜挎带与书袋、持纸草卷轴的青年史家。下半身要补出及膝袍摆+绑带凉鞋。

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Greek young male historian scholar, friendly confident smile, tousled dark brown hair, short trimmed beard and mustache, thin golden laurel wreath in the hair, white short-sleeved belted tunic with golden Greek-key trim at the collar and hem, navy-blue cloth sash draped over one shoulder with golden embroidered patterns and a round golden shoulder brooch with hanging golden leaf pendants, brown leather cross-body strap, ornate brown leather belt with a golden sun-star round buckle, brown leather satchel bag at the hip with golden compass-rose charms, tunic hem reaching the knees, bare forearms, holding a rolled papyrus scroll upright in one hand, strappy leather sandals with straps winding up the calves, feet visible, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

英文负向：（同上，通用负向清单）

中文版（即梦/豆包）：

一位古希腊青年史家学者的全身立绘。比例自然、约七到八头身、胯在画面中段；深棕色蓬松乱发、短须、自信友善的浅笑；发间戴一圈金色月桂细冠；身穿白色短袖束腰袍，领口与下摆金色回纹镶边；单肩斜披藏蓝色披巾，绣金色纹样，肩头金色圆形胸针垂金叶坠饰；胸前一条棕色皮革斜挎带，腰系宽皮带、正中金色星芒圆扣，胯侧挂一只棕色皮书袋、缀金色罗盘小坠；袍摆及膝，小臂裸露；一手竖持一卷纸草卷轴；小腿缠绑带式皮凉鞋。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

## ③ 神殿守卫（npc_greece_guardian）

立绘是金色科林斯盔配暗红盔缨、金色肌肉胸甲、红色披风、青铜护臂、红黑甲裙缀金月桂纹、持长矛与月桂徽记大圆盾的重装步兵。下半身要补出甲裙下白色衬裙+青铜护胫+战凉鞋。

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Greek hoplite temple guardian warrior, stern focused eyes, short dark beard on the jaw, golden Corinthian helmet with cheek guards and a tall dark-red horsehair crest, face partially visible through the helmet opening, muscular golden sculpted cuirass chest armor, red cape flowing behind the shoulders fastened with a round golden clasp, golden armband on the bare upper arm, bronze scaled forearm guards, red and black pteruges armored skirt with golden laurel-leaf ornaments on the straps, white pleated under-skirt showing beneath, bronze greaves on the shins, war sandals, feet visible, holding a tall bronze-tipped spear upright in one hand, large round bronze hoplite shield with a black laurel emblem and Greek-key meander ring border on the other arm, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

英文负向：（同上，通用负向清单）

中文版（即梦/豆包）：

一位古希腊神殿重装守卫的全身立绘。比例自然、约七到八头身、胯在画面中段；头戴金色科林斯头盔（带护颊、顶竖暗红色马鬃盔缨，盔口露出冷峻双眼与下颌短须）；身穿金色肌肉线条胸甲；肩后红色披风以金色圆扣固定；裸露的上臂戴金色臂环，双前臂青铜鳞纹护臂；腰下红黑相间的皮条甲裙（Pteruges），甲条上缀金色月桂叶饰，甲裙下露出白色百褶衬裙；小腿青铜护胫、脚穿战凉鞋；一手竖握一柄青铜矛尖的长矛，另一臂挽一面大圆青铜盾，盾面黑色月桂徽记、盾缘一圈回纹。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

---

# 罗马三 NPC（2026-07-06）

## ① 元老·马可（npc_rome_senator）

立绘是金色月桂冠、灰棕短发灰须、白色托加长袍配紫色金藤纹宽缘、金色太阳纹圆胸针、紫绳腰带缀金章流苏、持金帽卷轴的威严元老。下半身要补出袍摆及踝+深红色闭合元老皮靴。

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Roman elder senator statesman, dignified calm expression, short grey-streaked brown hair, neatly trimmed grey beard, golden laurel wreath on the head, white toga elegantly draped over a white tunic, wide purple border with golden vine and leaf embroidery along the drape, round golden sun-emblem brooch fastening the toga at the shoulder, golden engraved wide bracelets on the forearms, purple corded belt with a golden medallion and hanging purple tassels, toga hem reaching the ankles, closed dark-red senatorial leather boots, feet visible, holding a rolled scroll with golden caps in one hand, the other hand raised in a calm orator gesture, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

英文负向：（同上，通用负向清单）

中文版（即梦/豆包）：

一位古罗马元老政治家的全身立绘。比例自然、约七到八头身、胯在画面中段；灰棕色短发、修剪整齐的灰色胡须、神情沉稳威严；头戴金色月桂冠；身穿白色托加长袍叠白色内袍，袍缘一圈紫色宽边绣金色藤蔓叶纹；肩前金色太阳纹圆胸针固定袍褶；双前臂金色刻纹宽镯；腰间紫色绳结腰带缀金色圆章、垂紫色流苏；袍摆垂至脚踝，脚穿深红色闭合式元老皮靴（罗马元老专属红靴，非凉鞋）；一手持带金色端帽的纸卷，另一手自然抬起作演说手势。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

## ② 工程师·维特（npc_rome_engineer）

立绘是深棕乱发别金月桂枝、细髭山羊须、白色金紫边短袖束腰袍、蓝紫披巾缀金流苏与金日纹胸针、宽皮革工具腰带垂铅锤饰、皮革工具包、持图纸卷与青铜测量仪的青年工程师。下半身要补出白袍垂至小腿+棕色系带及踝工作皮靴。

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Roman young male engineer architect, confident friendly expression, messy dark brown hair with a small golden laurel sprig, thin mustache and short goatee, white short-sleeved belted tunic with golden and purple trim, blue-purple scarf cloak draped over one shoulder with golden fringe and a round golden sun-emblem brooch, wide brown leather tool belt with golden ornaments and hanging bronze plumb-bob pendants, brown leather satchel bag at the hip, bronze measuring ruler tucked at the belt, white tunic skirt reaching mid-shin, sturdy ankle-high brown laced leather work boots, feet visible, holding rolled architectural scrolls in one hand and an upright bronze groma surveying instrument in the other hand, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

英文负向：（同上，通用负向清单）

中文版（即梦/豆包）：

一位古罗马青年工程师/建筑师的全身立绘。比例自然、约七到八头身、胯在画面中段；深棕色蓬乱短发间别一小枝金色月桂、细髭与短山羊须、神情自信亲和；身穿白色短袖束腰袍，镶金紫双色边；单肩搭蓝紫色披巾，缀金色流苏与金色太阳纹圆胸针；腰系宽厚棕色皮革工具腰带，缀金饰、垂数枚青铜铅锤吊坠；胯侧挂棕色皮革工具包，腰间别一把青铜量尺；袍摆垂至小腿中段，脚穿棕色系带及踝工作皮靴（非凉鞋）；一手抱数卷建筑图纸，另一手竖持一具青铜测量仪（格罗马）。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

## ③ 斗兽场卫（npc_rome_guardian）

立绘是银色罗马头盔配红缨、红颈巾、银色板条环甲缀金狮金日圆章、棕皮交叉背带、红披风、剑臂银环甲护臂、红色铆钉甲裙、持短剑与金鹰翼纹大红盾的军团卫士。下半身要补出甲裙下青铜护胫+闭合式罗马军用皮靴。

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Roman legionary colosseum guard, stern resolute face, silver Roman galea helmet with golden trim, cheek guards and a tall red horsehair crest, red neck scarf, polished silver lorica segmentata banded plate armor with golden lion and sun medallions on the chest, brown leather cross baldric straps, red cape flowing behind the shoulders, segmented silver manica arm guard on the sword arm, wide leather belt with a golden buckle, red pteruges armored skirt studded with golden discs, bronze greaves on the shins, closed Roman military leather boots, feet visible, holding a short gladius sword in one hand, large red rectangular scutum shield with a golden eagle-wing emblem and a silver central boss on the other arm, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

英文负向：（同上，通用负向清单）

中文版（即梦/豆包）：

一位古罗马军团斗兽场卫士的全身立绘。比例自然、约七到八头身、胯在画面中段；面容坚毅冷峻；头戴银色罗马头盔（镶金边、带护颊、顶竖红色马鬃盔缨）；颈系红色围巾；身穿抛光银色板条环甲（罗马环片甲），胸前缀金狮与金日圆章，棕色皮革背带交叉胸前；肩后红色披风；持剑手臂套银色分段环甲护臂；腰系宽皮带配金扣；腰下红色皮条甲裙缀金色铆钉圆片；小腿青铜护胫，脚穿闭合式罗马军用皮靴（非凉鞋）；一手持罗马短剑，另一臂挽一面大型红色方盾，盾面金色鹰翼纹徽记、中央银色盾凸。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

# 丝路三 NPC（2026-07-06）

## ① 商队首领·阿罗（npc_trade_leader）

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Silk Road Sogdian caravan master, middle-aged merchant with a tanned weathered face, shrewd friendly smile, full dark beard, rounded felt hat with upturned brim, knee-length lapel-collar caftan robe in deep russet red with teal and gold pearl-roundel brocade trim on the lapels cuffs and hem, long sleeves, wide leather belt with a bronze buckle hung with coin pouches and a small sheathed knife, loose trousers tucked into closed brown leather riding boots, feet visible, one hand holding a camel lead rope, the other hand resting on the belt pouch, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

中文版（即梦/豆包）：

一位古丝绸之路粟特商队首领的全身立绘。比例自然、约七到八头身、胯在画面中段；中年男性，面容黝黑风霜、精明友善的笑容、络腮胡；头戴圆顶翻檐毛毡帽；身穿及膝翻领胡服长袍，深赭红色，翻领、袖口与下摆缀青绿与金色联珠纹锦缘；腰系宽皮带配青铜带扣，挂钱袋与小佩刀；宽松长裤塞进闭合式棕色皮革马靴（非凉鞋）；一手牵驼绳，一手按在腰间钱袋上。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

## ② 译经僧·法显（npc_trade_monk）

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 heads tall, hips at the middle of the figure, standing, elderly Chinese Buddhist pilgrim monk of the Silk Road, thin gentle face with deep kind wrinkles, serene faint smile, cleanly shaved head, grey-brown under robe with long sleeves, ochre saffron kasaya outer robe with rice-field grid pattern draped over the left shoulder leaving the right shoulder line visible, cloth leg wraps around the lower legs, closed dark cloth monk shoes, feet visible, wooden prayer beads around the neck, holding a rolled sutra scroll respectfully in both hands, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

中文版（即梦/豆包）：

一位古丝绸之路汉地行脚译经老僧的全身立绘。比例自然、约七头身、胯在画面中段；年迈清瘦，面容温和布满慈祥皱纹，神情宁静含笑；头顶剃净光头；内穿灰褐色长袖僧袍，外披赭黄色田相格纹袈裟、搭于左肩；小腿缠布绑腿，脚穿闭合式深色布面僧鞋（非凉鞋、非草鞋）；颈挂木质佛珠，双手恭敬捧一卷经卷。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。

## ③ 关隘守卫（npc_trade_guardian）

英文正向：

masterpiece, best quality, highly detailed, 1boy, solo, full body, full length, head to feet fully visible, natural well-proportioned body, about 7 to 8 heads tall, hips at the middle of the figure, standing, ancient Chinese Han dynasty frontier pass guard soldier of the Silk Road desert gate, stern wind-weathered face with sand-tanned skin, black hair tied under an iron helmet with a short red tassel on top and leather cheek guards, dark iron lamellar armor cuirass with rectangular overlapping plates laced with red cords over a crimson knee-length military robe, lamellar shoulder guards, wide leather belt with a bronze buckle, loose trousers tucked into closed black leather military boots, feet visible, both hands holding an upright long ji halberd with a bronze blade, small scarf against the sand around the neck, isolated on plain white background, simple background, flat even studio lighting, front view, full-body character reference, clean, anime style

中文版（即梦/豆包）：

一位古代汉代丝路关隘戍卒的全身立绘。比例自然、约七到八头身、胯在画面中段；面容坚毅、久经风沙、肤色黝黑；头戴铁盔，盔顶短红缨、皮质护颊，黑发束于盔下；身穿深铁色札甲（长方甲片红绳编缀），内衬绛红色及膝戎袍，肩覆札甲披膊；腰系宽皮带配青铜带扣；宽松长裤塞进闭合式黑色军用皮靴（非凉鞋）；颈围一条挡沙的小围巾；双手持一杆竖立的青铜长戟。

要求：完整全身、从头到脚不裁切、自然站立、平视镜头、纯白背景、均匀平光、画面干净；不要上长下短、不要短腿、不要多余的手或手臂、不要多人文字水印。二次元/3D角色风格，适合3D角色建模参考。
