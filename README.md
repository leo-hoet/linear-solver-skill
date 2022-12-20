# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg" card_color="#22A7F0" width="50" height="50" style="vertical-align:bottom"/> Linear Solver
Solves the rpp linear model and say the answer using [pareto front finder](https://github.com/giicis/pareto-front-finder).

For a complete comprehesion of what this test can do check the file `test/behage/linear-solver-skill.feature`

To run integration tests (assuming you have installed mycroft in a dev environment)

```bash
mycroft-start vktest -t linear-solver-skill
```


## Next steps
- Implement some type of visualization when users ask for a problem result. Maybe a web view?
- Improve the speech to text interface. Currently only support MVP phrases
- Make the model resolution async. This skill should call an external server to solve the model

## Credits
Leonardo Hoet

## Category
**Productivity**

## Tags
#Rpp
#Linear programming
#Research

