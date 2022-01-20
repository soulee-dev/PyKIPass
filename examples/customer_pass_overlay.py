from datetime import datetime, timedelta
from PyKIPass import *
import tkinter as tk
from typing import Callable, Any
import sys
import argparse


# source from https://github.com/notatallshaw/fall_guys_ping_estimate
class Overlay:
    """
    Creates an overlay window using tkinter
    Uses the "-topmost" property to always stay on top of other Windows
    """

    def __init__(self,
                 close_callback: Callable[[Any], None],
                 initial_text: str,
                 initial_delay: int,
                 get_new_text_callback: Callable[[], tuple[int, str]],
                 font_size
                 ):
        self.close_callback = close_callback
        self.initial_text = initial_text
        self.initial_delay = initial_delay
        self.get_new_text_callback = get_new_text_callback
        self.root = tk.Tk()

        # Set up Close Label
        self.close_label = tk.Label(
            self.root,
            text=' X |',
            font=('Consolas', font_size),
            fg='white',
            bg='black'
        )
        self.close_label.bind("<Button-1>", close_callback)
        self.close_label.grid(row=0, column=0)

        # Set up Ping Label
        self.ping_text = tk.StringVar()
        self.ping_label = tk.Label(
            self.root,
            textvariable=self.ping_text,
            font=('Consolas', font_size),
            fg='white',
            bg='black'
        )
        self.ping_label.grid(row=0, column=1)

        # Define Window Geometery
        self.root.overrideredirect(True)
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

    def update_label(self) -> None:
        wait_time, update_text = self.get_new_text_callback()
        self.ping_text.set(update_text)
        self.root.after(wait_time, self.update_label)

    def run(self) -> None:
        self.ping_text.set(self.initial_text)
        self.root.after(self.initial_delay, self.update_label)
        self.root.mainloop()


def now():
    return datetime.now()


def close(_):
    sys.exit()


def get_customer_count_dict(customer_count_list):
    customer_count_dict = {}

    for customer_count in customer_count_list:
        customer_count_dict[customer_count.time] = customer_count.total_customer_count

    return customer_count_dict


def trim_mean(arr, proportion_to_cut):
    nobs = len(arr)

    if nobs == 0:
        return []

    lower_cut = int(proportion_to_cut * nobs)
    upper_cut = nobs - lower_cut

    if lower_cut > upper_cut:
        ValueError("Proportion too big.")

    arr.sort()

    arr = arr[lower_cut:upper_cut]

    return int(sum(arr) / len(arr))


class CustomerCountOverlay:

    def __init__(self, username, password, max_week):
        self.kipass = KIPass(username=username, password=password)

        previous_customer_count_list = []

        for th_week in range(max_week):
            try:
                previous_customer_count_list.append(get_customer_count_dict(self.kipass.get_customer_count_on_day(
                    date=(now() - timedelta(days=7 * (th_week + 1))).strftime("%Y%m%d"))).get(now().strftime('%H'), 0))
            except ResponseIsNotSuccess:
                break

        self.previous_customer_count_trim_mean = trim_mean(previous_customer_count_list, 0.3)

    def update_text(self):
        today_customer_count_dict = get_customer_count_dict(self.kipass.get_customer_count_on_day(
            date=now().strftime("%Y%m%d")))

        text = f"{today_customer_count_dict.get(now().strftime('%H'), 0)} / " \
               f"{self.previous_customer_count_trim_mean} "

        return 5000, text

    def main(self, font_size):
        overlay = Overlay(close, "서버에 연결중 입니다 ", 500, self.update_text, font_size)
        overlay.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get customer count from WoW data")
    parser.add_argument("--username", "-u", type=str, help="Username of KIPass app", required=True)
    parser.add_argument("--password", "-p", type=str, help="Password of KIPass app", required=True)
    parser.add_argument("--font-size", "-f", type=int, default=20, help="Font size")
    parser.add_argument("--max-week", "-m", type=int, default=8, help="Set maximum week")

    args = parser.parse_args()

    customer_count_overlay = CustomerCountOverlay(args.username, args.password, args.max_week)
    customer_count_overlay.main(args.font_size)

print('wow')