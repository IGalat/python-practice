# Tapper
Finally, some good f* hotkey utility!

...hopefully.

Features:
- Keyboard/mouse controlling and monitoring
- Hotkeys, on release`*`, on hold`*`, hotstrings`*`
- Per-app actions
- Selective key suppression
- Intuitive high-level interface
- Cross-platform`*`
- Language support`*`
- Suspension of tapper or chosen actions
- Custom conditions for triggering in addition to hotkey
- Auto-fire while pressed/toggled`*`

`*` - not implemented yet

### Installation

Not implemented yet :) 

At this stage, create your_script.py in src/ folder. Usual imports are

``` python
from tapper import Tapper
from util.controller import Controller as Ct
```
and perhaps:
``` python
from key import Keys
from tap import Tap
```

### Usage

See `EXAMPLE.py` for working code example.

Simplest example:

``` python
Tapper({"e": "r", "r": "e", "app": ""}).start()
```

This swaps keys "e" and "r", and disables an "app" key.
Works with any modifiers, so `control + E` will become `control + R` etc.

`tapper.start()` is the last command in script as it is blocking, so no commands after will be executed.

See `key.Keys` for list of keys.

#### Groups

To separate and better control your hotkeys, use groups:

``` python
tapper = Tapper()

tapper.group({"e": "r", "r": "e"}, "remap")
tapper.group([Tap("alt+f7", lambda: Ct.mouseover(1850, 1000))], "mouse")

tapper.start()
```

Last parameter is group name, so "remap" and "mouse" can be used to refer to groups.

Now pressing `alt + F7` will move your cursor to `x=1850, y=1000`.

The single hotkey of group "mouse" can be written in dict form, like "remap" is:

``` python
tapper.group({"alt+f7": lambda: Ct.mouseover(1850, 1000)}, "mouse")
```

Action can be a separate function:

``` python
def moveToCoords():
    Ct.mouseover(1850, 1000)

tapper.group({"alt+f7": moveToCoords}, "mouse")
```

Now you can use all of Python's power in executing the hotkey!

Creating `Tap()` instead of just dict gives you additional flexibility:

``` python
def moveToCoords():
    Ct.mouseover(1850, 1000)

tapper.group([Tap("alt+f7", moveToCoords
                  , suppress_trigger_key_on_action=False
                  , no_additional_keys=True)
              ], "mouse")
```

Now if you press `alt + F7`, the key itself will be propagated to your OS before the action.

And `no_additional_keys` means that if you also have, say, `shift` pressed, action won't trigger.

#### Suspending

Let's say you want to disable your "remap" or "mouse" group with a hotkey.

``` python
tapper.group({"e": "r", "r": "e"}, "remap")

tapper.group({"alt+f7": lambda: Ct.mouseover(1850, 1000)}, "mouse")

tapper.group({
    "num2": tapper.suspend_groups("remap"),
    "num8": tapper.unsuspend_groups("remap"),
    "num5": tapper.toggle_suspend_groups("mouse")
}, "suspending")
```

Now when you press `Numpad 2`(down arrow on numpad), "remap" will stop working until you press `Numpad 8`;
and `Numpad 5` will toggle suspension of "mouse" group - that is, suspend it the first time, and unsuspend the second.

#### Actions

So what can you do with `Controller` (`Ct`)?

`send` is a versatile command:

- `Ct.send("Hello, World!")` - will type this text
- `Ct.send("Hello,$(enter)World!")` - parses keys inside of `$()`, so this will be printed on two lines
- `Ct.send("Hello,$(shift down)people$(shift up) of Earth!` - special `down`/`up` modifier will only press/release a key
- `Ct.send("Hello, $(ctrl+v) World!")` - parses hotkey. This will paste your clipboard between `Hello, ` and ` World!`
- `Ct.send("$(lmb)")` - mouse clicks are no different, this will click left mouse button at its current position
- (TODO make mouse special modifier for xy coords)

Use `Ct.pressed(Keys.a)` to see if `a` is pressed

`Ct.toggled(Keys.caps)` - is caps lock on?

`Ct.release_all_keys()` - releases keys you press, so they don't interfere with actions. 
Useful for actions with modifiers

---

`Ct.get_mouse_pos()` - returns tuple(x,y)

`Ct.mouseover(newX, newY)` - you can only specify one, such as `Ct.mouseover(y=500)`, and x will be preserved

`Ct.move_mouse_delta(dX, dY)` - moves relative to current cursor position (TODO work with one coord like mouseover)

`click` - will mouse over a spot and then send keys:

- `Ct.click("qwerty", 400, 600)` - will mouseover x=400, y=600, and send `qwerty`
- `Ct.click("$(rmb), y=250)` - will mouseover x=current x, y=250, and click right mouse button

---

And, finally, window actions

`get_open` - returns list of opened visible windows, with optional filter. (TODO also return windows in tray)

- `Ct.get_open("chrome")` - will return windows whose exe file or title contains "chrome".
So Google Chrome("chrome.exe"), but also if you have a file "my-colors-black-and-chrome.txt" opened in Notepad, will be fetched.
- `Ct.get_open(exec = "chrome")` - will only fetch Google Chrome, from previous example
- `Ct.get_open(title = "Youtube - Google Chrome")` - will only return Google Chrome window if Youtube is current tab.

Usually you won't need windows themselves, but this can be used as a condition:
``` python
if Ct.get_open(exec = "chrome"):
    do_my_thing()
```

`get_fore` - returns foreground window, with same filters as `get_open`.

`set_fore` - switches foreground window. You must specify some filters for it to know what you want.

If you got a window from `get_open` or `get_fore`, use `Ct.set_fore(handle = found_window.handle)`.

Or just `Ct.set_fore("chrome")`

#### Per-window hotkeys and custom conditions

This will only work when "chrome" is in foreground:

``` python
tapper.group({"f1": "$(ctrl+t)"}, "chrome", trigger_if=lambda: Ct.get_fore("chrome"))
```

so now rather useless `F1` opens a new tab, and `shift + F1` opens last closed tab, as it becomes `shift + ctrl+t`.

Works on individual TAPs too:

``` python
tapper.group([
    Tap("ctrl+y", "$(ctrl+shift+z)", trigger_if=lambda: Ct.get_fore("idea"))
    # some other Taps
], "salad")
```

and now in "idea" you can press `ctrl+y` to revert last `ctrl+z`, like in other editors.

(note that action key combo requires `$()` to be parsed while hotkey doesn't)

---

You can use any custom function for `trigger_if`:

``` python
def my_condition():
    return Ct.get_fore(title="Youtube - Google Chrome") or Ct.get_fore(exec="wmplayer.exe") or some_other_condition()

tapper.group({"up_arrow": lambda: Ct.click("$(lmb+lmb)", 600, 600)}, "videos", trigger_if=my_condition)
```

This will try to go fullscreen by double-clicking where your video hopefully is, in youtube or windows media player or in some other case you specify.



### Order of triggering

Only one hotkey is triggered per keypress.

First, control group is checked. Then other groups, in order of you adding them.
Inside a group, taps will be checked in order of adding.

So, here

``` python
gr1 = tapper.group({"1": "q",      "ctrl+1": "w"})
gr2 = tapper.group({"ctrl+1": "a", "2": "s"})
```

`"ctrl+1": "w"` from `gr1` will never trigger, because `"1": "q"` will trigger first.

`"ctrl+1": "a"` from `gr2` will never trigger, because `"1": "q"` from gr1 will trigger first.

However, if `"1": "q"` is suspended or has `trigger_if` condition that isn't satisfied,
`"ctrl+1": "w"` can now be triggered.

If it, or the whole `gr1`, is also not suspended/not `trigger_if`ing,
`"ctrl+1": "a"` from `gr2` can now be triggered.


### Controls 

Tapper has built-in default controls: 

- F2 terminates the script
- control + F2 restarts it
- F1 suspends/unsuspends hotkey triggering

To make your own controls:

``` python
from util.tap_control import TapControl

tapper.controlGroup.add({"f4": TapControl.terminate_script, 
                         "ctrl+f5": TapControl.restart_script, 
                         "f5": lambda: tapper.toggle_suspend})
```

Adding any control will prevent default controls from being added.

Control group is always active and ignores suspension.

### Config

Config.controller_interval_sec can be changed to introduce delay between controller key actions.