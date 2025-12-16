from openai import OpenAI
geo = '{"type": "Feature","geometry": {"type": "Point","coordinates": [121.8255503,24.9051011]},"properties": {"fclass": "peak","name": "太和山"}}'

# client = OpenAI(
#     api_key='sk-00141ef3447840dda7bc7f06f7318d9d',
#     base_url="https://api.deepseek.com")
#
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "你是一名军事专家,请你对user的问题进行专业详细的回答"},
#         {"role": "user", "content": f"geojson数据如下:{geo},高程数据为海拔694m左右,请你根据上述geojson和高程数据通过research总结出其所具有的地理态势特征和周围地理地标特征的关系及其所具有的军事作战价值,给出一份简介的军事报告"},
#     ],
#     stream=False
# )

# 火山引擎联网deepresearch
client = OpenAI(
    api_key='cdf0d0c8-b8c5-4665-a631-5c40db8322da',
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots")

response = client.chat.completions.create(
    model="bot-20251204164109-vr5ts",
    messages=[
        {"role": "system", "content": "你是一名军事专家,请你对user的问题进行专业详细的回答"},
        {"role": "user", "content": "geojson数据如下:[{'1730': {'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [[121.181528, 24.9462903], [121.181446, 24.9461621], [121.1811475, 24.9458223], [121.1811509, 24.9457436], [121.1812223, 24.9456788], [121.1817601, 24.9454442], [121.1821022, 24.9453409], [121.1833173, 24.944648], [121.1833895, 24.9446364]]}, 'properties': {'fclass': 'service', 'id': 1730}}}, {'3117': {'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [[121.1725493, 24.957458], [121.1737603, 24.9576885]]}, 'properties': {'fclass': 'service', 'name': '民族路五段147巷4弄', 'id': 3117}}}, {'2371': {'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [[121.1485577, 24.9375366], [121.1487173, 24.9375476], [121.1488339, 24.9375768], [121.1488996, 24.9375865], [121.1489761, 24.9375743], [121.1490472, 24.9375488], [121.149089, 24.9374088], [121.1495404, 24.9373572], [121.1499358, 24.9372351], [121.1499813, 24.9372291], [121.1500354, 24.9372506], [121.1500942, 24.9373254], [121.1501786, 24.9374071], [121.1503, 24.9374552], [121.1504728, 24.9376143], [121.1513311, 24.9382028], [121.1514227, 24.9383216]]}, 'properties': {'fclass': 'service', 'id': 2371}}}, {'330': {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[121.1602935, 24.9765893], [121.1605281, 24.9764994], [121.1606284, 24.9766149], [121.1606074, 24.9766239], [121.1606807, 24.9767255], [121.1604084, 24.9768685], [121.1602935, 24.9765893]]]}, 'properties': {'fclass': 'farmland', 'id': 330}}}, {'868': {'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [[121.182939, 24.9226502], [121.1828571, 24.9223671]]}, 'properties': {'fclass': 'tertiary', 'name': '梅獅路一段', 'id': 868}}}],,请你根据上述geojson数据结合搜寻出来的信息总结出其所具有的地理态势特征(坡度,地形类型,地形特征,交通位置)和周围地理地标特征的关系(地标与我所提供数据的相对位置要准确,不可以随便生成。也不要使用id代替地点名称。)及其所具有的军事作战价值,给出一份简洁的军事报告"},
        # {"role": "user", "content": f"geojson数据如下:{geo},高程数据为海拔694m左右,请你根据上述geojson和高程数据总结出其所具有的地理态势特征和周围地理地标特征的关系(地标与我所提供数据的相对位置要准确,不可以随便生成)及其所具有的军事作战价值,给出一份简介的军事报告"}
    ],
)

print(response.choices[0].message.content)