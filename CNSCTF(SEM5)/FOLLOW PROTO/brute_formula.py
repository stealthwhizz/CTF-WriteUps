key_digits = [1, 3, 7, 7, 9]
required_shifts = [13, 4, 19, 22, 14]

print("Brute force search for formula:")
print(f"Key: {key_digits}")
print(f"Target: {required_shifts}")
print()

# Try different formulas with constants a, b, c
# Formula: (a * i + b) * k + c

found = False
for a in range(-5, 20):
    for b in range(-5, 20):
        for c in range(-5, 30):
            match = True
            calculated = []
            for i in range(len(key_digits)):
                val = ((a * i + b) * key_digits[i] + c) % 26
                calculated.append(val)
                if val != required_shifts[i]:
                    match = False
                    break
            
            if match:
                print(f"FOUND! a={a}, b={b}, c={c}")
                print(f"Formula: ((a * i + b) * k + c) % 26 = (({a} * i + {b}) * k + {c}) % 26")
                print(f"Calculated: {calculated}")
                found = True
                break
        if found:
            break
    if found:
        break

if not found:
    print("No simple formula found. Trying other patterns...")
    print()
    
    # Try: a * i^2 + b * i + c * k + d
    for a in range(-3, 5):
        for b in range(-3, 15):
            for c in range(-3, 5):
                for d in range(-3, 20):
                    match = True
                    calculated = []
                    for i in range(len(key_digits)):
                        val = (a * i * i + b * i + c * key_digits[i] + d) % 26
                        calculated.append(val)
                        if val != required_shifts[i]:
                            match = False
                            break
                    
                    if match:
                        print(f"FOUND! a={a}, b={b}, c={c}, d={d}")
                        print(f"Formula: (a * i^2 + b * i + c * k + d) % 26")
                        print(f"        = ({a} * i^2 + {b} * i + {c} * k + {d}) % 26")
                        print(f"Calculated: {calculated}")
                        found = True
                        break
                if found:
                    break
            if found:
                break
        if found:
            break
