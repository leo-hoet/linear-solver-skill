from dataclasses import dataclass
from io import StringIO
from typing import List

@dataclass
# duplicated from pareto_front_finder
class RunResult:
    iteration: int
    profit: float
    cost: float
    x: str
    y: str
    time: float
    pid: int


class HtmlTableConstructor:
    @staticmethod
    def _table_headers() -> str:
        headers = StringIO("")
        headers.write("<thead>")
        headers.write("<tr>")
        headers.write("<th>Name")
        headers.write("</th>")
        headers.write("<th> Implemented")
        headers.write("</th>")
        headers.write("</tr>")
        headers.write("</thead>")
        headers.seek(0)
        return headers.read()


    @staticmethod
    def construct(req_names: List[str], x: List[str]) -> str:
        table = StringIO("")
        table.write("<table>")
        table.write(HtmlTableConstructor._table_headers())

        table.write("<tbody>")
        for req_name, x_ in zip(req_names,x):
            table.write("<tr>")
            table.write(f"<td>{req_name}</td>")
            table.write(f"<td>{x_}</td>")
            table.write("</tr>")
        table.write("</tbody>")
        table.write("</table>")
        table.seek(0)
        return table.read()



def run_result_to_html(data: RunResult) -> str:
    html = StringIO('')

    reqs_name = [f'Req {i}' for i in range(len(data.x))]
    stackholders_name = [f'Stakeholder {i}' for i in range(len(data.x))]
    reqs_table = HtmlTableConstructor.construct(reqs_name, [c for c in data.x])
    stakeholder_table = HtmlTableConstructor.construct(stackholders_name, [c for c in data.y])

    html.write(f"<h1>Profit: {data.profit} </h1>")
    html.write(f"<h1>Cost: {data.cost} </h1>")
    html.write(f"<h3>Time: {data.time} </h3>")
    html.seek(0)
    html = html.read()
    return html + reqs_table + stakeholder_table

def main():
    data = RunResult(
        1, 123.1, 454.2345, '1001', '1345634', 0.001,1
    )
    html = run_result_to_html(data)
    with open('/dev/shm/data_demo.html', 'w') as f:
        f.write(html)




if __name__ == "__main__":
    main()