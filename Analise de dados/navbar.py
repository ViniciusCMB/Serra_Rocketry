from dash import html


def create_navbar():
  """Cria a barra de navegação do aplicativo."""

  # Cria a logo da barra de navegação
  logo = html.Img(src='assets/LOGO - SEM TEXTO.png',
                  style=dict(width='100px', height='100px', flex='none', marginLeft='10px'))

  # Cria o título da barra de navegação
  titulo = html.H1('Serra Rocketry', style=dict(
      flex='auto', marginLeft='10px'))

  # Cria a seção de links de navegação (cada link é uma página do aplicativo, mais páginas podem ser adicionadas)
  links = html.Nav([
      html.A('Home', href='/'),
      html.A('Ignitor', href='/ignitor'),
      html.A('Análise teste estático', href='/analise_teste_estatico'),
      html.A('Análise voo', href='/analise_voo')], style=dict(display='flex', marginRight='15px'))

  # Cria o cabeçalho da barra de navegação
  navbar = html.Header([logo, titulo, links], className='card', style=dict(
      borderRadius='0px', margin='0px', marginBottom='10px', border='0px', borderBottom='2px solid #232333'))

  return navbar
