from bs4 import BeautifulSoup
from pathlib import Path
import base64, gzip, sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
soup = BeautifulSoup(path.read_text(encoding="utf8"), "html.parser")

THICK_GZ_B64 = "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"
BOX_GZ_B64 = "H4sIACouymoC/7VbS28cyZG++1cU6MvMQa18PwzLB9d4tg9N+LBrHngZCCNqREAWBYq2NP9+vy8iH1XNXs3s2IYAFb/KzHhlZkRkZPUfP/3zp+Xz/Zund6+urE9Xy7u7+5/ePTXwz/u7z39++PLqyixmwZtF3r69f//+1dWHhw93V8uXv7//8OnV1bunp49/ePny8+fPh8/+8PD400tnjHkJ4ld/+t0fP75+ere8eXV1bRZnj9bGG9A5mhtnbzu13+fy/fchXr38dd3/8fj+m99/fH3/4cn88Pj6zf3r9z/4H5wp3+4JYCxInPgQEifT4UVa9hdpmYMIcxJbQDBz6q8vkHM/vL//cPf68TI5pXAYNOyW8EV6/pfomaPzp240IWUukAn/HjLxa2RqODhb8+LDoRpQq/lgU6mLKwdrTFqBnaHW5WC8cwtxdIvLh1oLkXfGN3is6GQLBuFZUh29SCuUSQPP7HzncarxYG1xXYYV2JSYBKccFmKfyuLjAnFrthA3Hil5IjM8DZq01Zbs5sC9crfX1nj+xRe2Br8Sex1QvAuLNe6QSP1goyW0h1xLx+huDtXFTbs5OAzrw2s9pOrDIA9sk8N4f4jRWypeasZ4cInJTWwP0fi6DmwOPhS/9PGuHkLEJHT6MFyxPq6dPw2ZYdguH+xeok1D/obXpt5sVu3ncLXOJB8OwfvBnjjRHE28gZv4Azf1+viu/pn1dTqcMnA1VZGvJBEAYheZDl9EvxhqmfooXomddZt2c8h+Ox6Sxjzow361QBDgXLGKKp+xUqHo4gbbQ6jSXaE7BK7XPhz6YCMN6oDZJLt27p4L0qi0lA44hOLmalK8du1mu2o/x6t1Jn1/SKZM9p7iDekGVuEHbLr10V33M9tzMiJmS4wTixg3HjwIEPtMfmg30h6qSYqlmdKfrEmH6sVxeEi/Co4yFw6TvQguMncuJQ7PBxOyYJvZH57HqONJIi9wUOxl8dAzKYZHOhG7JONNtl7G+2wFOxelf0jDUxHG0B0VUeV+RmeoMvrQQU0/tcH0UzfdP/X33c10Ml651kD3JPL5rHrRxcSm0mbYgKB6A0PaaMKJdi2yyYytUaahWMWxqNkz9BTsrGIKY05nMzhDtv0L/+0df4APq3R5lsurHAXbcGzvb68Td7Ud7YRHfXd77bDGDHe45VrMK7DnYhNMBwQcamunBYFtUmYuROnvXW7YaX96FOmfBSff8emM3e014k6WGWv8ibMf7AlDJ+8lTGU7mBO5Ti047W3rYE4cU+nMz3hB+QQmOU7lU9uvXfmECTdxKg/sc57KA8cwdU9c12nqDlxCGrrvuWGfinuQ4JERdVaLfQR5G4YR4KVsC04G+9bRK4WgG97mI/qX6hLHuZyruKXKcRErl2YCtthY5BM7Wi1nvqbRiiVmjNEYwpkF5hZf53sGEWoB90NlzUGEY4SWzEnwCqbJ20175mIugrEcF0tvYdQbVIPdUCi0biW6YuLIhWY4aUGw5VwCJ+5wepOg/RO3IHYqlFcsyDZflI7NsDey4+IRi46NN9Y6kD7CrMHVfOLTGJW4JmhQ4SVLVA2imB+pQBWc6ceq5iCCXWZ/G0xrJ52KfZxdaxeNao1WMdgBhm4gV6mQ0cXrQBeGStg5rq0WunXPyRwY81F8SLM9YSekohPgYmlYpk7/1EBSkl3gP7N0RVxC/Fm4vpwEGkhWmU0gTUPcqgwQ4ing8FPpC3M5W6i31yHAIoinfeUGRARGkr5yA5ZMNLkR9Es04hEHwwg3EGoYAkWYoC3BMqAVXUYTo0dd5sgqQWpQhszOhLVzplURk7pg3Whd8G7U4LCou7tju0Fa5cdwjyWQ0yDuGaFKHsw9k2axowo3cVrn36qTji1D5U66WaQz7hZTwdKYgjOLi1M33A99ChIUqNWNKUjMbKsfBFNCjK+DX+Ium9Ik5F02zBmYGF3H36rlGKpG6ISbjTrfZsEu1li1Tew+ARHz5Ysd7ZG5hRvDI7yKulClHgMSLcaHPv1IhTz3YF8eA2PljL/bqpKxm0XXafdF2ViPRSuijVW/nFn89hqB28JHcYCLK7K1mqxTxNTOOyQ5TPRzldzAyUIDM/jmlQcPl9QrM6kDTkbcG/SWM1DHAc4rrxPDpcEAoJeN+jvEEmGnBwFmLehOs3uFiAyESCVbHhQEi7MmRoZIbCU1o5d10u4UOq8weh3u6skzb5EcQPwpWpG/5JOnX/OabGXrVk+3VxUzBQBONepuiUWxqiT4iPhoSq6rQ/gabxcgXSCkwiSWOKssWOfdqTsI4Wy8Eesf28zcXmc0iufi61OGY/S1r56yEuekHhrn0gW4pB6ziGp26u/tMWfJXFY8m09HDwQb40obHwV7Ca1C/1QsJr9k5X4s4RCrKadc21yp5BlnYpf9KcHBM43Wzk1wSZCC7RrccLmElI8FsQfnx7Uw5kRdRni/FAYZr+fdCCttMU7bN1xOWLzrfI+cFTOtdIIsL4O5avQ7PrKYgL43ejYIF/jL+w0/ngnSDiMXupFghSRkvAcOyLAGf2DaZvAXnI/NCn22CzIrl9tkt7YZlXqmAx9qfTu+MdOBj4U+UTMdMJlY/G/7G8sKR7kxtqUzM3BouhMyk4XZzFwiujlcsEaC2dbYtqFdqr3U07N3NeCHgq9hDICfQh5hB72JxYe1v1WOMbbJOd2vqpHkRJpmO7a29WWMV6z+dLYp3zG2yXUmN/Jb9msJEWL4Shcf24ZyJAqnhQR3aYuCOMppjbjk9UL7+fgtfSwAEDBOJ8lGLABEANcyNgsrAOfYrMH8HrhU21Mou15oPx+/pX97HbFnpdLZGEbZ934MSPALqQx6yWge1fmdNZ+PPqMOg2JRJhoE/qUEHBiQGzmj+YhENuBiW3JkBCOl7KHanyyTisbA2MjxIcXmD0tl/2C80q/0ixxvd+O3/CEQlnKRIz5cvhxE4Nn8PDIA29ZceCDhQaVoO06m64X2Z+Mnecwvi2JBSwC5rAELLnptRoKwBFZpGvkAuwEHq1saXn290LwfvqOOyeWxv/kucAP0qSd76A4cGeE7ucjDqE+D3YX28/Eb8qzaIL7lJl5lGYYlONewPZ21ywCnx7zMqhyzeFedyi9RjMU9rycoocOiTxgpwvPm89Fb6nJYZnjW0ALX0cO0oBamBdIHzChtGW8kbmDlrfM9HBXiDoloYpKUzGAi+OhkS0TmEsV6P/qxUOlDFuy9lM6MRiueLYFilLJPlCzeaWRlsGPesYGIbevEemzX0V5SsYho3mnL4l8nZ6s1wiFZM4RK3HHPaqTSEq2U6yLoy9k0hqrPKM3eZtXBx3BshZZjey/THVhzlXQ2sswG1240mlU5SPNA0TJGSUKQgcoEMvVcLzSfD9+Sx2ZD5hqKlMIzckWGscpSOWunAZsy0gnL5oR3QoIWSUAPGAG5FWBOTrPrRGeG3WaC1lorxAJ2Lmj0cEmOhPt2GR/n+Gfkd9z30qXlTHpEVS7XPLTBqQXCdV2AYgh+UAMupp3OyC2xMiOOT4VJdFw+DGGBMdduKHOhfT/+nP5z/kO6tOxFx1IxLWxxSfp6FOzSsb2/vWbQD804JI9M2qkrYp3b4fyfIJ2Kw/eFgdzExp79z9vPx5/T96HPFXeOlHqc9me84K1E6oddY1dp937TzvF2M35HHyetKjnyYOhZ6jZu2As4ttOzWMwzHqYx2Reaz4fvyRceLtOQx7OoEOKQFzhnG4c+F9r34/f0EVoivdZmNcMH1LLZSywct3sKChxbJbEr9Kxdxpft+HP6Ti8mVCBgm7wdAkfe0xk7FLrQfj5+Sx8T5CBI0HuuHORAiQmW4y8yMzlw4kCmmCewdvNBmEM4Aap2vuhgxwsHYu4SGez1CMTgccZMi8i8ceDJHD71KPjY3u6qVU6qVQHcfOyYGbjleZaYfCUtjNLucQpZtT3OdhkftuO39He1GWGYeBJ2oz9gKJOcZIXBDnbPm3eD97RnBV/ud2cBnxA55ijgEzMu9QI+cUAO2gv4gm0ZBXzpn8oo4As28bRnN2vonX0roQ/2rYQ+2LcS+mCvJfTBvZXQB/e+8Dv3HTcJUiTTuRPaEgZ3YPizwZwQucxgTpxtGtyle3aDO8kZZwf3PTfMM/PnXDp3wmAHc0Jr8uAO7Fmm79yJq95aCHf2N7UM7sTMRzv3PTdwzzwVjIkn9GZOPLGUPjp7xCC5Su/sgYufE09c65x4jrdhTvye3by9KG5/e6F43l4U5BtUu99eFIy3qTy7vSiIcp4JaLu9KHFzeaFg3F0otOPuomS9HODdRTXj6qI6HiNCv7qoYXdzoXBcXAhk0GoXF/wEQU6f7eKiWuaWflxcABdv3bi4AM5ynGgXF8BJvkxoFxfEntcJ7eICONY6ry4aHpcXhWcs4H57UdOlywt+RpF4m9AuL6hF9PPyotI38YzcLi+ImaH0ywti4/O4vJB21j3a5QVxqnHcXpC+q3bcXkAqZxna2+1FldmdtxeKy7i9aHjcXvDDjojI0m4vMHn98gJzWhKCbL+8KIlVWzcuL7CueKc/Li+K319etHW5nK3TWbYtflu2FTTKtkC7si2YhWzyKNtiAbrIMmwry0K4gKx9Yp3UUbblZGaeU7RsW+2uasulFbLvVVvC3IIkc14sYyOHnFa1Ja45j6ptdduiLRB6lVG0JZ41W11F5yVb9EF6WkfJFjjBDqNkCxzle4lWslV8VrHtnXrFlkTku4F25uNu9L6t416vFbPPeq1c3yD0yusbWBlrphx5OeJLZpEuMrjo+8oTO3ZqJo657DDX0E3p11P9PcsOmGulk6XqyC8SGv2G3RFSQIh8U40s4mf89X0e/DBhhvnqBtPD3MiHTSkN/sCBVdHOHxjTHwd/xenYrNBM5XG4yM43U7U2CT4mF3tmqih3HZ6XHxgThql4GSLeuJlKsX9mqvG+mWrQaaZq9IepkI5kHvC7qc75d1N1/t1Unc+5qUa/ZqpBp5mq8++malZopuKhseJQraZqbRIpAy9N5PUpwzVZ3SgxlrQSR1of6xVrPrMqEHUP0HLAUmUUnI+ZX0IFjAoyK61bZrdUgm6VGDqWGBRsbhLxEgGDm7TCyTpG1sj6HzxeCLxCo8uDjQq/g4EP5WkSboCQJdqshQKFR4ZtOGAeIbEV0+gFDkwWhGa0DUtzLH0TJrlbSt1caqVZt5Xv8fi5Uqu7Esv1SavL6pyVUbclLtmuF9rPx2/pz7pmxeQiFRl1TWIaoNc1K786Y7BqdU1iuKlR16zUB3PT65ps577rdU1ihpRe19yM3/JvdU12gF9MUQubkpMzoahVC5s62cgXyyhsAlckW+uF9mfjN/Rn8Y+rpbpZ/BNs3emsfRb/mDVEl0fxj1lGkesyre4xSxGOrfrXQ82F9vPxW/qz/EcHgo3ffL6iUf4DRKrjh8und4FXoXeQg9AIBYbVPzfKf8CR3qUzUeyelf96v16EA/ZeK3xGfJRkaL38BxxSraPgB59WWM7fYPqwUQAskvnOAiCCeqypFxd554RFMgqA1M3zA9Ym2zBFKwA2Qz0vAEIsfuN4I8/SnrXMEmDhBWGIz0uAgUka4x+cNfQWp40s76ZhiQku6zXc5Q6yDIx0gHetWhW0Ygpr5SYBywJnEmL5CgeYBypgHBJaFVFaTdWaIUuMMFwtUtrUGiJTt1j4AdyO26xc0ZYIeP935Yr5ls9xVK6APb+R65WpQtdS/ahcFeb0Ja7P28/Hn9PXyhXvZpE1jcoVMObajcoVk00D/XvlSttn5UrHu3P6szACF7srjNDlbgsjxJvCCOEsjADtCiPE28KIDN4URhqz22vEm8oVj9y3Rp4p2KHqM/LKNPOwg3lmcszKieAQju29LDnLL4B7h3aEPrb3suQ8E4reoZ1yj+39xU8X39y9/YSHfvn/X3zcfXha7t+8urrw+4Kr5Uf+GgKPn+Xx+OrKXi0/tVF/+3D/9OnV1T8+3T3+98fXP9799cPfPt3N5v95fP3h09uHx7+/unrin+9fP919g/nN9dvl8eGJ6EXhd7TJfrt8+vH1+7tvrGRn/DaYYcx9y19TfHp6+Ljwvxc/Prx/eNz/dkIaH96+/XT3JKLt+iEYfGeM9Hu51/crBrD/YQNI9X4YgOUnX3+T+vryAXzvn0S4f80e+uuG5/bY/6rjavli249lfrZikS9OHj+79vrrtrmokP1zztb9BoU2C+HlXv6vKOQvKWSjKiQqfOm6/CtKef/dd879sg7G/OX7XC4r/+uVCheUeuEQS5taCPZRFYtW9XoR+OY3KPZrd9/XZvXXKxYvzZb8ZCXfvTC5qVe7di94CWlqQltVPc1/VMn/3+y9bM6XPxT70+/+F+7LRC6MNgAA="

thick = gzip.decompress(base64.b64decode(THICK_GZ_B64)).decode("utf8")
box = gzip.decompress(base64.b64decode(BOX_GZ_B64)).decode("utf8")

def svg_uri(svg_text):
    return "data:image/svg+xml;base64," + base64.b64encode(svg_text.encode("utf8")).decode("ascii")

thick_dark = thick.replace('fill="white"', 'fill="#1E1E1E"')
thick_white = thick

gray_map = {
    "#78FF45":"#F1F1F1",
    "#69FF31":"#E3E3E3",
    "#17C200":"#AFAFAF",
    "#10B000":"#8B8B8B",
    "#6DFF38":"#E7E7E7",
    "#4DF61A":"#C9C9C9",
    "#059700":"#292929",
    "#75FF41":"#DADADA",
    "#076B00":"#303030",
    "#74FF3F":"#E1E1E1",
    "#28D608":"#A8A8A8",
    "#C4FFAC":"#F6F6F6",
}
box_gray = box
for old, new in gray_map.items():
    box_gray = box_gray.replace(old, new)

thick_dark_uri = svg_uri(thick_dark)
thick_white_uri = svg_uri(thick_white)
box_gray_uri = svg_uri(box_gray)

light_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="480" height="251" viewBox="0 0 480 251">
  <style>
    .display { font-family: Arial, Helvetica, sans-serif; font-weight: 700; fill: #1E1E1E; }
    .mono { font-family: 'Courier New', monospace; fill: #1E1E1E; }
  </style>
  <image href="__THICK_DARK__" x="18" y="18" width="238" height="80" preserveAspectRatio="xMidYMid meet"/>
  <image href="__BOX_GRAY__" x="266" y="12" width="106" height="106" preserveAspectRatio="xMidYMid meet"/>
  <text class="mono" x="382" y="43" font-size="17">BUILT TO</text>
  <text class="mono" x="382" y="70" font-size="17">&lt;/&gt; FLEX</text>
  <text class="mono" x="18" y="151" font-size="20">THE VAULT  &gt;&gt;&gt;  GREEN GROOVE</text>
  <text class="mono" x="18" y="205" font-size="20">TO LEVEL UP</text>
  <g stroke="#1E1E1E" stroke-width="5" stroke-linecap="square">
    <path d="M201 179V227"/><path d="M177 203H225"/><path d="M184 186L218 220"/><path d="M218 186L184 220"/>
  </g>
  <text class="mono" x="254" y="206" font-size="20">20</text>
  <path d="M296 198H393" stroke="#1E1E1E" stroke-width="3"/>
  <text class="mono" x="416" y="206" font-size="20">25</text>
</svg>""".replace("__THICK_DARK__", thick_dark_uri).replace("__BOX_GRAY__", box_gray_uri)

dark_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="880" height="142" viewBox="0 0 880 142">
  <style>
    .big { font-family: Arial, Helvetica, sans-serif; font-weight: 700; fill: #F2F2F2; }
    .mono { font-family: 'Courier New', monospace; fill: #F2F2F2; }
  </style>
  <text class="big" x="8" y="41" font-size="48">SMART BINS</text>
  <text class="big" x="331" y="41" font-size="42">ROUTE OPTIMIZATION</text>
  <image href="__BOX_GRAY__" x="78" y="51" width="62" height="62" preserveAspectRatio="xMidYMid meet"/>
  <text class="big" x="166" y="93" font-size="43">WASTE, IOT</text>
  <text class="big" x="515" y="93" font-size="49">⌘</text>
  <text class="big" x="574" y="93" font-size="43">COMMUNITY</text>
  <text class="mono" x="177" y="128" font-size="17">DESIGNED + ENGINEERED BY</text>
  <rect x="530" y="103" width="151" height="35" rx="17.5" fill="none" stroke="#F2F2F2" stroke-width="2"/>
  <image href="__THICK_WHITE__" x="557" y="105" width="98" height="33" preserveAspectRatio="xMidYMid meet"/>
</svg>""".replace("__BOX_GRAY__", box_gray_uri).replace("__THICK_WHITE__", thick_white_uri)

replacements = {
    "osmo-micrographic-2.avif": (svg_uri(light_svg), "Green Groove identity graphic"),
    "osmo-micrographic-3.avif": (svg_uri(dark_svg), "Green Groove smart bins, route optimization, waste IoT and community"),
}

updated = 0
for img in soup.find_all("img"):
    src = img.get("src", "")
    for needle, (replacement, alt) in replacements.items():
        if needle in src:
            img["src"] = replacement
            img["alt"] = alt
            img.attrs.pop("srcset", None)
            img.attrs.pop("sizes", None)
            updated += 1
            break

if updated != 2:
    raise RuntimeError(f"Expected 2 Osmo micrographic replacements, got {updated}")

path.write_text(str(soup), encoding="utf8")
print("Installed Green Groove replacements for Osmo micrographics 2 and 3.")