from bs4 import BeautifulSoup
from pathlib import Path
import base64, gzip, hashlib, sys
import brand_apply as base

path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
s = BeautifulSoup(path.read_text(encoding="utf8"), "html.parser")

# Exact user-supplied `gg logo.svg`, compressed only for transport in the build.
LOGO_GZ_B64 = "H4sIAPXUyWoC/7VbS28cyZG++1cU6MvMQa18PwzLB9d4tg9N+LBrHngZCCNqREAWBYq2NP9+vy8iH1XNXs3s2IYAFb/KzHhlZkRkZPUfP/3zp+Xz/Zund6+urE9Xy7u7+5/ePTXwz/u7z39++PLqyixmwZtF3r69f//+1dWHhw93V8uXv7//8OnV1bunp49/ePny8+fPh8/+8PD400tnjHkJ4ld/+t0fP75+ere8eXV1bRZnj9bGG9A5mhtnbzu13+fy/fchXr38dd3/8fj+m99/fH3/4cn88Pj6zf3r9z/4H5wp3+4JYCxInPgQEifT4UVa9hdpmYMIcxJbQDBz6q8vkHM/vL//cPf68TI5pXAYNOyW8EV6/pfomaPzp240IWUukAn/HjLxa2RqODhb8+LDoRpQq/lgU6mLKwdrTFqBnaHW5WC8cwtxdIvLh1oLkXfGN3is6GQLBuFZUh29SCuUSQPP7HzncarxYG1xXYYV2JSYBKccFmKfyuLjAnFrthA3Hil5IjM8DZq01Zbs5sC9crfX1nj+xRe2Br8Sex1QvAuLNe6QSP1goyW0h1xLx+huDtXFTbs5OAzrw2s9pOrDIA9sk8N4f4jRWypeasZ4cInJTWwP0fi6DmwOPhS/9PGuHkLEJHT6MFyxPq6dPw2ZYdguH+xeok1D/obXpt5sVu3ncLXOJB8OwfvBnjjRHE28gZv4Azf1+viu/pn1dTqcMnA1VZGvJBEAYheZDl9EvxhqmfooXomddZt2c8h+Ox6Sxjzow361QBDgXLGKKp+xUqHo4gbbQ6jSXaE7BK7XPhz6YCMN6oDZJLt27p4L0qi0lA44hOLmalK8du1mu2o/x6t1Jn1/SKZM9p7iDekGVuEHbLr10V33M9tzMiJmS4wTixg3HjwIEPtMfmg30h6qSYqlmdKfrEmH6sVxeEi/Co4yFw6TvQguMncuJQ7PBxOyYJvZH57HqONJIi9wUOxl8dAzKYZHOhG7JONNtl7G+2wFOxelf0jDUxHG0B0VUeV+RmeoMvrQQU0/tcH0UzfdP/X33c10Ml651kD3JPL5rHrRxcSm0mbYgKB6A0PaaMKJdi2yyYytUaahWMWxqNkz9BTsrGIKY05nMzhDtv0L/+0df4APq3R5lsurHAXbcGzvb68Td7Ud7YRHfXd77bDGDHe45VrMK7DnYhNMBwQcamunBYFtUmYuROnvXW7YaX96FOmfBSff8emM3e014k6WGWv8ibMf7AlDJ+8lTGU7mBO5Ti047W3rYE4cU+nMz3hB+QQmOU7lU9uvXfmECTdxKg/sc57KA8cwdU9c12nqDlxCGrrvuWGfinuQ4JERdVaLfQR5G4YR4KVsC04G+9bRK4WgG97mI/qX6hLHuZyruKXKcRErl2YCtthY5BM7Wi1nvqbRiiVmjNEYwpkF5hZf53sGEWoB90NlzUGEY4SWzEnwCqbJ20175mIugrEcF0tvYdQbVIPdUCi0biW6YuLIhWY4aUGw5VwCJ+5wepOg/RO3IHYqlFcsyDZflI7NsDey4+IRi46NN9Y6kD7CrMHVfOLTGJW4JmhQ4SVLVA2imB+pQBWc6ceq5iCCXWZ/G0xrJ52KfZxdaxeNao1WMdgBhm4gV6mQ0cXrQBeGStg5rq0WunXPyRwY81F8SLM9YSekohPgYmlYpk7/1EBSkl3gP7N0RVxC/Fm4vpwEGkhWmU0gTUPcqgwQ4ing8FPpC3M5W6i31yHAIoinfeUGRARGkr5yA5ZMNLkR9Es04hEHwwg3EGoYAkWYoC3BMqAVXUYTo0dd5sgqQWpQhszOhLVzplURk7pg3Whd8G7U4LCou7tju0Fa5cdwjyWQ0yDuGaFKHsw9k2axowo3cVrn36qTji1D5U66WaQz7hZTwdKYgjOLi1M33A99ChIUqNWNKUjMbKsfBFNCjK+DX+Ium9Ik5F02zBmYGF3H36rlGKpG6ISbjTrfZsEu1li1Tew+ARHz5Ysd7ZG5hRvDI7yKulClHgMSLcaHPv1IhTz3YF8eA2PljL/bqpKxm0XXafdF2ViPRSuijVW/nFn89hqB28JHcYCLK7K1mqxTxNTOOyQ5TPRzldzAyUIDM/jmlQcPl9QrM6kDTkbcG/SWM1DHAc4rrxPDpcEAoJeN+jvEEmGnBwFmLehOs3uFiAyESCVbHhQEi7MmRoZIbCU1o5d10u4UOq8weh3u6skzb5EcQPwpWpG/5JOnX/OabGXrVk+3VxUzBQBONepuiUWxqiT4iPhoSq6rQ/gabxcgXSCkwiSWOKssWOfdqTsI4Wy8Eesf28zcXmc0iufi61OGY/S1r56yEuekHhrn0gW4pB6ziGp26u/tMWfJXFY8m09HDwQb40obHwV7Ca1C/1QsJr9k5X4s4RCrKadc21yp5BlnYpf9KcHBM43Wzk1wSZCC7RrccLmElI8FsQfnx7Uw5kRdRni/FAYZr+fdCCttMU7bN1xOWLzrfI+cFTOtdIIsL4O5avQ7PrKYgL43ejYIF/jL+w0/ngnSDiMXupFghSRkvAcOyLAGf2DaZvAXnI/NCn22CzIrl9tkt7YZlXqmAx9qfTu+MdOBj4U+UTMdMJlY/G/7G8sKR7kxtqUzM3BouhMyk4XZzFwiujlcsEaC2dbYtqFdqr3U07N3NeCHgq9hDICfQh5hB72JxYe1v1WOMbbJOd2vqpHkRJpmO7a29WWMV6z+dLYp3zG2yXUmN/Jb9msJEWL4Shcf24ZyJAqnhQR3aYuCOMppjbjk9UL7+fgtfSwAEDBOJ8lGLABEANcyNgsrAOfYrMH8HrhU21Mou15oPx+/pX97HbFnpdLZGEbZ934MSPALqQx6yWge1fmdNZ+PPqMOg2JRJhoE/qUEHBiQGzmj+YhENuBiW3JkBCOl7KHanyyTisbA2MjxIcXmD0tl/2C80q/0ixxvd+O3/CEQlnKRIz5cvhxE4Nn8PDIA29ZceCDhQaVoO06m64X2Z+Mnecwvi2JBSwC5rAELLnptRoKwBFZpGvkAuwEHq1saXn290LwfvqOOyeWxv/kucAP0qSd76A4cGeE7ucjDqE+D3YX28/Eb8qzaIL7lJl5lGYYlONewPZ21ywCnx7zMqhyzeFedyi9RjMU9rycoocOiTxgpwvPm89Fb6nJYZnjW0ALX0cO0oBamBdIHzChtGW8kbmDlrfM9HBXiDoloYpKUzGAi+OhkS0TmEsV6P/qxUOlDFuy9lM6MRiueLYFilLJPlCzeaWRlsGPesYGIbevEemzX0V5SsYho3mnL4l8nZ6s1wiFZM4RK3HHPaqTSEq2U6yLoy9k0hqrPKM3eZtXBx3BshZZjey/THVhzlXQ2sswG1240mlU5SPNA0TJGSUKQgcoEMvVcLzSfD9+Sx2ZD5hqKlMIzckWGscpSOWunAZsy0gnL5oR3QoIWSUAPGAG5FWBOTrPrRGeG3WaC1lorxAJ2Lmj0cEmOhPt2GR/n+Gfkd9z30qXlTHpEVS7XPLTBqQXCdV2AYgh+UAMupp3OyC2xMiOOT4VJdFw+DGGBMdduKHOhfT/+nP5z/kO6tOxFx1IxLWxxSfp6FOzSsb2/vWbQD804JI9M2qkrYp3b4fyfIJ2Kw/eFgdzExp79z9vPx5/T96HPFXeOlHqc9me84K1E6oddY1dp937TzvF2M35HHyetKjnyYOhZ6jZu2As4ttOzWMwzHqYx2Reaz4fvyRceLtOQx7OoEOKQFzhnG4c+F9r34/f0EVoivdZmNcMH1LLZSywct3sKChxbJbEr9Kxdxpft+HP6Ti8mVCBgm7wdAkfe0xk7FLrQfj5+Sx8T5CBI0HuuHORAiQmW4y8yMzlw4kCmmCewdvNBmEM4Aap2vuhgxwsHYu4SGez1CMTgccZMi8i8ceDJHD71KPjY3u6qVU6qVQHcfOyYGbjleZaYfCUtjNLucQpZtT3OdhkftuO39He1GWGYeBJ2oz9gKJOcZIXBDnbPm3eD97RnBV/ud2cBnxA55ijgEzMu9QI+cUAO2gv4gm0ZBXzpn8oo4As28bRnN2vonX0roQ/2rYQ+2LcS+mCvJfTBvZXQB/e+8Dv3HTcJUiTTuRPaEgZ3YPizwZwQucxgTpxtGtyle3aDO8kZZwf3PTfMM/PnXDp3wmAHc0Jr8uAO7Fmm79yJq95aCHf2N7UM7sTMRzv3PTdwzzwVjIkn9GZOPLGUPjp7xCC5Su/sgYufE09c65x4jrdhTvye3by9KG5/e6F43l4U5BtUu99eFIy3qTy7vSiIcp4JaLu9KHFzeaFg3F0otOPuomS9HODdRTXj6qI6HiNCv7qoYXdzoXBcXAhk0GoXF/wEQU6f7eKiWuaWflxcABdv3bi4AM5ynGgXF8BJvkxoFxfEntcJ7eICONY6ry4aHpcXhWcs4H57UdOlywt+RpF4m9AuL6hF9PPyotI38YzcLi+ImaH0ywti4/O4vJB21j3a5QVxqnHcXpC+q3bcXkAqZxna2+1FldmdtxeKy7i9aHjcXvDDjojI0m4vMHn98gJzWhKCbL+8KIlVWzcuL7CueKc/Li+K319etHW5nK3TWbYtflu2FTTKtkC7si2YhWzyKNtiAbrIMmwry0K4gKx9Yp3UUbblZGaeU7RsW+2uasulFbLvVVvC3IIkc14sYyOHnFa1Ja45j6ptdduiLRB6lVG0JZ41W11F5yVb9EF6WkfJFjjBDqNkCxzle4lWslV8VrHtnXrFlkTku4F25uNu9L6t416vFbPPeq1c3yD0yusbWBlrphx5OeJLZpEuMrjo+8oTO3ZqJo657DDX0E3p11P9PcsOmGulk6XqyC8SGv2G3RFSQIh8U40s4mf89X0e/DBhhvnqBtPD3MiHTSkN/sCBVdHOHxjTHwd/xenYrNBM5XG4yM43U7U2CT4mF3tmqih3HZ6XHxgThql4GSLeuJlKsX9mqvG+mWrQaaZq9IepkI5kHvC7qc75d1N1/t1Unc+5qUa/ZqpBp5mq8++malZopuKhseJQraZqbRIpAy9N5PUpwzVZ3SgxlrQSR1of6xVrPrMqEHUP0HLAUmUUnI+ZX0IFjAoyK61bZrdUgm6VGDqWGBRsbhLxEgGDm7TCyTpG1sj6HzxeCLxCo8uDjQq/g4EP5WkSboCQJdqshQKFR4ZtOGAeIbEV0+gFDkwWhGa0DUtzLH0TJrlbSt1caqVZt5Xv8fi5Uqu7Esv1SavL6pyVUbclLtmuF9rPx2/pz7pmxeQiFRl1TWIaoNc1K786Y7BqdU1iuKlR16zUB3PT65ps577rdU1ihpRe19yM3/JvdU12gF9MUQubkpMzoahVC5s62cgXyyhsAlckW+uF9mfjN/Rn8Y+rpbpZ/BNs3emsfRb/mDVEl0fxj1lGkesyre4xSxGOrfrXQ82F9vPxW/qz/EcHgo3ffL6iUf4DRKrjh8und4FXoXeQg9AIBYbVPzfKf8CR3qUzUeyelf96v16EA/ZeK3xGfJRkaL38BxxSraPgB59WWM7fYPqwUQAskvnOAiCCeqypFxd554RFMgqA1M3zA9Ym2zBFKwA2Qz0vAEIsfuN4I8/SnrXMEmDhBWGIz0uAgUka4x+cNfQWp40s76ZhiQku6zXc5Q6yDIx0gHetWhW0Ygpr5SYBywJnEmL5CgeYBypgHBJaFVFaTdWaIUuMMFwtUtrUGiJTt1j4AdyO26xc0ZYIeP935Yr5ls9xVK6APb+R65WpQtdS/ahcFeb0Ja7P28/Hn9PXyhXvZpE1jcoVMObajcoVk00D/XvlSttn5UrHu3P6szACF7srjNDlbgsjxJvCCOEsjADtCiPE28KIDN4URhqz22vEm8oVj9y3Rp4p2KHqM/LKNPOwg3lmcszKieAQju29LDnLL4B7h3aEPrb3suQ8E4reoZ1yj+39xU8X39y9/YSHfvn/X3zcfXha7t+8urrw+4Kr5Uf+GgKPn+Xx+OrKXi0/tVF/+3D/9OnV1T8+3T3+98fXP9799cPfPt3N5v95fP3h09uHx7+/unrin+9fP919g/nN9dvl8eGJ6EXhd7TJfrt8+vH1+7tvrGRn/DaYYcx9y19TfHp6+Ljwvxc/Prx/eNz/dkIaH96+/XT3JKLt+iEYfGeM9Hu51/crBrD/YQNI9X4YgOUnX3+T+vryAXzvn0S4f80e+uuG5/bY/6rjavli249lfrZikS9OHj+79vrrtrmokP1zztb9BoU2C+HlXv6vKOQvKWSjKiQqfOm6/CtKef/dd879sg7G/OX7XC4r/+uVCheUeuEQS5taCPZRFYtW9XoR+OY3KPZrd9/XZvXXKxYvzZb8ZCXfvTC5qVe7di94CWlqQltVPc1/VMn/3+y9bM6XPxT70+/+F+7LRC6MNgAA"
logo_svg = gzip.decompress(base64.b64decode(LOGO_GZ_B64))
assert hashlib.sha256(logo_svg).hexdigest() == "b76419769aa9ee5510dfd8f9c33a36e9a2b61a5e66b6d134d008db843284bc47"
logo_uri = "data:image/svg+xml;base64," + base64.b64encode(logo_svg).decode("ascii")

# Persist the exact cube mark as the site's favicon and use it wherever the source UI
# collapses the brand down to an icon-only treatment (not the wide wordmark).
Path("favicon.svg").write_bytes(logo_svg)
for svg in s.select("svg.nav-logo__icon-svg"):
    svg.clear()
    svg["viewBox"] = "0 0 136 136"
    svg["preserveAspectRatio"] = "xMidYMid meet"
    image = s.new_tag("image", attrs={
        "href": logo_uri, "x": "0", "y": "0", "width": "136", "height": "136",
        "preserveAspectRatio": "xMidYMid meet"
    })
    svg.append(image)

# The footer is a wide signature placement, so use the horizontal wordmark rather than
# squeezing the square cube mark into the source's long logo slot.
footer_slots = s.select(".footer-bottom__logo")
for slot in footer_slots:
    if slot.name == "svg":
        base.embed_svg_asset(slot, base.wordmark_uri, "0 0 170 15", 170, 15)
    else:
        slot.clear()
        img = s.new_tag("img", attrs={
            "src": base.wordmark_uri,
            "alt": "Green Groove",
            "class": "gg-footer-wordmark"
        })
        img["style"] = "display:block;width:100%;height:auto;object-fit:contain;object-position:left center;"
        slot.append(img)

path.write_text(str(s), encoding="utf8")
print(f"Applied cube mark to {len(s.select('svg.nav-logo__icon-svg'))} compact nav slot(s); horizontal wordmark to {len(footer_slots)} footer slot(s); exact cube favicon written.")
