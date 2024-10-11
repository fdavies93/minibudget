import render

def render_table():
    table = render.Table()
    
    for column_name in ['A','B','C','D']:
        column = render.TableColumn()
        column.align = render.Alignment.LEFT
        column.add_cell(f"\033[1m{column_name}\033[22m")
        for i in range(5):
            column.add_cell(f"{"\t" * i}{column_name * i}")
        table.columns.append(column) 
    lines = table.render(render.RenderOptions(80, "", 2))
    print('\n'.join(lines))

def main():
    render_table()

if __name__ == "__main__":
    main()
