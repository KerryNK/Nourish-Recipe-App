from django.contrib.auth.models import User

print("Adding full names to users...")
print("-" * 60)

# Map of usernames to full names
user_names = {
    'testuser123': ('John', 'Doe'),
    'favtest': ('Jane', 'Smith'),
    'shoptest': ('Mike', 'Johnson'),
    'reviewtest': ('Sarah', 'Williams'),
}

for username, (first_name, last_name) in user_names.items():
    try:
        user = User.objects.get(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        print(f"✓ {username:<15} → {first_name} {last_name}")
    except User.DoesNotExist:
        print(f"✗ User '{username}' not found")

print("\n" + "=" * 60)
print("Done! Users now have full names.")
print("\nCurrent users:")
print("-" * 60)
for user in User.objects.all():
    full_name = user.get_full_name() or "No full name"
    print(f"{user.username:<15} → {full_name}")
