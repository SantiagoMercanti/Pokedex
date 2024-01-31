import flet as ft
import aiohttp 
import asyncio

pokemon_actual = 0

async def main(page: ft.Page):
    page.window_width = 720 * 2/3
    page.window_height = 1280 * 2/3 
    page.window_resizable = False
    page.padding = 0

    async def peticion(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
            

    async def evento_get_pokemon(e: ft.ContainerTapEvent):
        global pokemon_actual
        if e.control == flecha_superior:
            pokemon_actual += 1
        else:
            pokemon_actual -= 1
        numero = (pokemon_actual%150)+1
        resultado = await peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}")

        datos = f"Name: {resultado['name'].capitalize()}\n\nAbilities: "
        for elemento in resultado['abilities']:
            habilidad = elemento['ability']['name'].capitalize()
            datos += f"\n{habilidad}"
        datos += f"\n\nHeight: {resultado['height']}"
        texto.value = datos
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        imagen.src = sprite_url

        await page.update_async()

    async def blink():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()

    luz_azul = ft.Container(width=70*2/3, height=65*2/3, left=4, top=5, bgcolor=ft.colors.BLUE, border_radius=50)

    boton_azul = ft.Stack([
        ft.Container(width=80*2/3, height=80*2/3, bgcolor=ft.colors.WHITE, border_radius=50),
        luz_azul,
    ])

    items_superior = [
        ft.Container(boton_azul, width=80*2/3, height=80*2/3),
        ft.Container(width=40*2/3, height=40*2/3,  bgcolor=ft.colors.RED_200, border_radius=50),
        ft.Container(width=40*2/3, height=40*2/3,  bgcolor=ft.colors.YELLOW, border_radius=50),
        ft.Container(width=40*2/3, height=40*2/3,  bgcolor=ft.colors.GREEN, border_radius=50),

    ]

    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png"
    imagen = ft.Image(
        src = sprite_url,
        scale = 10,
        width=35*2/3,
        height=35*2/3,
        top = 350/3,
        right = 550/3,
    )   

    stack_central = ft.Stack([
        ft.Container(width=600*2/3, height=400*2/3, bgcolor=ft.colors.WHITE, border_radius=20),
        ft.Container(width=550*2/3, height=350*2/3, bgcolor=ft.colors.BLACK, top=25*2/3, left=25*2/3),
        imagen
    ])

    triangulo = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(40*2/3,0),
            ft.canvas.Path.LineTo(0,50*2/3),
            ft.canvas.Path.LineTo(80*2/3,50*2/3),
        ],
        paint=ft.Paint(
            style=ft.PaintingStyle.FILL,
            ),
        ),
    ],
    width=80*2/3,
    height=50*2/3
    )

    flecha_superior = ft.Container(triangulo, width=80*2/3,height=50*2/3, on_click=evento_get_pokemon)

    flechas = ft.Column(
        [
            flecha_superior,
            ft.Container(triangulo, rotate=ft.Rotate(angle=3.14159), width=80*2/3,height=50*2/3, on_click=evento_get_pokemon),
        ]
    )

    texto = ft.Text(
        value="...",
        color=ft.colors.BLACK,
        size=14
    )

    items_inferior = [
        ft.Container(width=50*2/3), #MArgen izquierdo
        ft.Container(texto, padding=10,width=400*2/3, height=300*2/3, bgcolor=ft.colors.GREEN, border_radius=20),
        ft.Container(width=20*2/3), #MArgen derecho
        ft.Container(flechas, width=80*2/3, height=120*2/3),      

    ]

    superior = ft.Container( content=ft.Row(items_superior), width=600 * 2/3, height=80 * 2/3, margin=ft.margin.only(top=40))
    centro = ft.Container(content=stack_central, width=600 * 2/3, height=400* 2/3, margin=ft.margin.only(top=40), 
                          alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior), width=600 * 2/3, height=400* 2/3, margin=ft.margin.only(top=40))


    col = ft.Column(spacing=0, controls=[
        superior,
        centro,
        inferior,
    ])

    contenedor = ft.Container(col, width=720* 2/3, height=1280* 2/3, bgcolor=ft.colors.RED, alignment=ft.alignment.top_center)

    await page.add_async(contenedor)
    await blink()


ft.app(target=main)