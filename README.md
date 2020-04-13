<h1 align="center">
  <br>
  <a href="http://autonom.io"><img src="https://raw.githubusercontent.com/autonomio/trauma-team-international/master/logo.png" alt="Talos" width="350"></a>
  <br>
</h1>

<h3 align="center">Trauma Team International - Coronavirus Taskforce</h3>

<p align="center">
  <a href="#sos-what">what?</a> •
  <a href="#gem-why">why?</a> •
  <a href="#wrench-how">how?</a> •
  <a href="#how-to-get-involved">how to get involved?</a> •
  <a href="https://autonom.io">About Autonomio</a> •
  <a href="https://github.com/autonomio/talos/issues">Issues</a> •
  <a href="#License">License</a>
</p>
<hr>
<p align="center">
Trauma Team International is an open collective focused on <strong>providing critically important insights</strong> to coronavirus decision makers. 
</p>

### :sos: what?

Trauma Team International use research and statistical methods to answer critically important questions about prevention of Coronavirus, and its effects on the healthcare system. 

Questions we are focused on answering and providing insights for include: 

>*1) "we have x ventilators / ventilator operators and have y patients immediately needing ventilation, but x is smaller than y, who is least likely to survive"*

>*2) "how can you avoid things escalating to the level where ventilator is needed in the first place."*
<hr>

>*3) "let number of people dying from COVID-19 be `x`, how can we make `x` smaller instead of just changing the time distribution?"

>*4) "what behaviors and mitigation effects yield the most favorable balance between economic, psychological, and health outcomes?"

**Methods:** 

- make available meaningful datasets for other reseachers
- make available a tool that dramatically increase access to literature
- make available statistical and machine learning models for other researchers

**Contributions:**

- [Behavioral Mitigation Simulator](https://github.com/autonomio/pandemik)
- [Intensive Care Unit Capacity Simulation](https://github.com/autonomio/ICUSIM)
- [Intensive Care Unit Burden Dataset](https://github.com/autonomio/trauma-team-international/tree/master/data)
- [RK4-based SEIR for Python](https://github.com/autonomio/trauma-team-international/blob/master/SEIR/rk4.py)
- [Bayesian COVID-19 Forecasting](https://github.com/autonomio/trauma-team-international/blob/master/icu_burden/icu_burden_bayesian.py)
- ["What Can COVID-19 Forecasters Learn from Pascal’s Wager"](https://towardsdatascience.com/what-can-covid-19-forecasters-learn-from-pascals-wager-acb010f347e0)

### :gem: why?

In many countries, healthcare systems have already been stretched thin and are not well prepared to take on the surge of coronavirus patients. Intensive Care Units (ICUs) are particularly at risk, due to limitations pertaining to ventilation machines and staff qualified to operate such machines. Once there are more patients needing ventilation than there are available ventilators or people capable of operating ventilators, patients that could otherwise been saved, will die. 

<hr>

### :wrench: how?

To answer these critically important questions, we leverage three gold standard methods:

- Literature and desk research
- Quantitative data analysis
  - Descriptive analysis
  - Statistical analysis
  - Machine learning
- Monte Carlo simulation
- Data visualization

At the moment, we have several work in progress or open research tracks: 

- [ ] perform a cursory literature view on COVID-19
- [ ] use MIMIC-III dataset to evaluate pneumonia and ventilation in ICU context
- [ ] create a simulation model for evaluating healthcare system burden scenarios

<hr>

### 💬 How to get involved

| I want to...                     | Go to...                                                  |
| -------------------------------- | ---------------------------------------------------------- |
| **...connect with others**      | [Discord]                                            |
| **...read the wiki**           | [Wiki]                                  |
| **...suggest something**  | [GitHub Issue Tracker]                                     |

<hr>

### 📢 Citations

If you use Trauma Team International's research, data, or findings for published work, please cite:

`Autonomio. (2019). Retrieved from http://github.com/trauma-team-international/talos.`

<hr>

### 📃 License

[MIT License](https://github.com/autonomio/talos/blob/master/LICENSE)

[github issue tracker]: https://github.com/automio/trauma-team-international/issues
[wiki]: https://github.com/autonomio/talos/wiki
[discord]: https://discord.gg/t7vk27
