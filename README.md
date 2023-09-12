
An experiment on visualizing runtime graphs (`graph.xxx.dot`) from the pants build tool. See [Debugging: Visualize the rule graph](https://www.pantsbuild.org/docs/rules-api-tips#debugging-visualize-the-rule-graph).

## Build and install

To build this tool:
```shell
$ pants package ::
...
15:18:14.73 [INFO] Wrote dist/pants_graph_view.pex
```
and if you want you can add the pex somewhere on your `$PATH`

## Usage

You can try it out in the example-python repo:
```text
example-python $ pants --engine-visualize-to=dist/ test ::
...
✓ helloworld/greet/greeting_test.py:tests succeeded in 0.71s.
✓ helloworld/translator/translator_test.py:tests succeeded in 0.71s.
15:20:53.12 [INFO] Visualizing graph as graph.005.dot

example-python $ pants_graph_view.pex dist/graph.005.dot
Writing to dist/graph.005.html
```
and then open the html file in your browser. `open dist/graph.005.html` would suffice on mac.

## Example files
