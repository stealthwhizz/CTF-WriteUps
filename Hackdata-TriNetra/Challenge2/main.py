from secret import verify

print("TriNetra watches silently...")
x = input("Speak the sacred phrase: ")

if verify(x):
    print("TriNetra accepts.")
else:
    print("TriNetra rejects.")

