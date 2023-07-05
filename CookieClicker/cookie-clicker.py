#  Principals of Computing, Rice university
#  Cookie Clicker Simulator
#  Written in Python 2.0

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 10000.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0,None,0.0,0.0)]

    def __str__(self):
        """
        Returns human readable state
        """
        return ("Total cookies: " + str(self._total_cookies) +
                ". \nCurrent cookies: " + str(self._current_cookies) +
                ". \nCurrent CPS: " + str(self._current_cps) +
                ". \nCurrent time: " + str(self._current_time))

    def get_cookies(self):
        """
        Returns current number of cookies
        (not total number of cookies)
        """
        return self._current_cookies

    def get_cps(self):
        """
        Gets current CPS
        """
        return self._current_cps

    def get_time(self):
        """
        Gets current time
        """
        return self._current_time

    def get_history(self):
        """
        Returns history list

        a list of tuples of the form:
        (time, item, cost of item, total cookies)
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Returns time until you have the given number of cookies
        """
        if self._current_cookies >= cookies:
            return 0.0

        cookies = cookies - self._current_cookies
        return math.ceil(cookies / self._current_cps)

    def wait(self, time):
        """
        Waits for given amount of time and updates state
        """
        if time > 0.0:
            self._current_time += time
            self._total_cookies += time * self._current_cps
            self._current_cookies += time * self._current_cps

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buys an item and updates state
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    info = build_info.clone()
    clicker = ClickerState()

    while clicker.get_time() <= duration:
        if clicker.get_time() > duration:
            break

        time_left = duration - clicker.get_time()
        stg_item = strategy (clicker.get_cookies(), clicker.get_cps(), clicker.get_history(), time_left, info)

        if not stg_item:
            break

        time = clicker.time_until(info.get_cost(stg_item))
        if time > time_left:
            break

        else:
            clicker.wait(time)
            while clicker.get_cookies() >= info.get_cost(stg_item):
                clicker.buy_item(stg_item, info.get_cost(stg_item), info.get_cps(stg_item))
                info.update_item(stg_item)

    clicker.wait(time_left)

    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    returns cursor
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cookies += time_left * cps
    least_price = float('inf')
    cheapest_item = None

    for item in build_info.build_items():
        item_price = build_info.get_cost(item)
        if (item_price < least_price) and (item_price <= cookies):
            least_price = item_price
            cheapest_item = item

    return cheapest_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cookies += time_left * cps
    highest_price = 0.0
    items = build_info.build_items()

    most_item = None
    for item in items:
        item_price = build_info.get_cost(item)

        if (item_price <= cookies) and (item_price > highest_price):
            highest_price = item_price
            most_item = item

    return most_item


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy.
    """
    cookies += time_left * cps
    top_ration = 0.0
    top_option = None

    items = build_info.build_items()
    for item in items:
        item_price = build_info.get_cost(item)

        if cookies >= item_price:
            ratio = build_info.get_cps(item) / item_price

            if ratio > top_ration:
                top_ration = ratio
                top_option = item

    return top_option


def run_strategy(strategy_name, time, strategy):
    """
    Simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time
    history = state.get_history()
    print history
    history = [(item[0], item[3]) for item in history]

    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """

    run_strategy("Best", SIM_TIME, strategy_best)


run()
