import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
time_available = st.number_input("Available time (minutes)", min_value=1, value=120)
pet_name = st.text_input("Pet name", value="Mochi")
pet_age = st.number_input("Pet age", min_value=1, value=1)
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    if 'owner' not in st.session_state:
        st.session_state.owner = Owner(name=owner_name, time_available=time_available)
    pet = Pet(species=species, name=pet_name, age=pet_age)
    st.session_state.owner.add_pet(pet)
    st.success(f"Added pet {pet_name}")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if 'owner' in st.session_state and st.session_state.owner.pets:
    if "scheduler" not in st.session_state:
        st.session_state.scheduler = Scheduler(st.session_state.owner)
    
    pet_options = [f"{pet.name} ({pet.species})" for pet in st.session_state.owner.pets]
    selected_pet_index = st.selectbox("Select pet for task", range(len(pet_options)), format_func=lambda i: pet_options[i])
    selected_pet = st.session_state.owner.pets[selected_pet_index]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_description = st.text_input("Task description", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"], index=0)

    if st.button("Add task"):
        task = Task(pet=selected_pet, description=task_description, time=duration, frequency=frequency)
        st.session_state.scheduler.add_task(task)
        st.success(f"Added task {task_description}")

if 'scheduler' in st.session_state and st.session_state.scheduler.tasks:
    st.write("Current tasks:")
    st.table([{"description": t.description, "time": t.time, "frequency": t.frequency, "pet": t.pet.name} for t in st.session_state.scheduler.tasks])
else:
    st.info("No tasks yet. Add a pet and tasks above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if 'scheduler' in st.session_state:
        schedule = st.session_state.scheduler.calculate_daily_schedule()
        if schedule:
            st.write("Today's Schedule:")
            total_time = 0
            for task in schedule:
                st.write(f"- {task.description} for {task.pet.name} ({task.time} min)")
                total_time += task.time
            st.write(f"Total time: {total_time} min (out of {st.session_state.owner.time_available} min available)")
        else:
            st.info("No tasks fit the schedule or no tasks available.")
    else:
        st.warning("Add pets and tasks first.")
