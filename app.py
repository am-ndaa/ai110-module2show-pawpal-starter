import streamlit as st
from pawpal_system import Owner, Pet, Task, Priority, Scheduler
from datetime import time
from rag_utils import build_rag_answer, load_knowledge_base

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
🐾 **PawPal+** helps you plan and organize pet care tasks for the day.

Enter your pet info, add tasks, and let the scheduler optimize your daily pet care routine!
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

st.subheader("📋 Your Pet Information")

col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
with col3:
    species = st.selectbox("Species", ["dog", "cat", "hamster", "other"])

col1, col2 = st.columns(2)
with col1:
    pet_age = st.number_input("Pet age (years)", min_value=1, max_value=30, value=3)
with col2:
    available_hours = st.number_input("Available hours/day", min_value=1, max_value=24, value=8)

st.markdown("### 📝 Add Tasks")
st.caption("Create tasks for your pet with priority levels.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task name", value="Morning walk")
with col2:
    task_type = st.selectbox("Task type", ["exercise", "feeding", "enrichment", "grooming", "training", "other"])
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("➕ Add task"):
    st.session_state.tasks.append({
        "name": task_title,
        "type": task_type,
        "duration_minutes": int(duration),
        "priority": priority
    })
    st.success(f"Added '{task_title}' to task list!")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if st.session_state.tasks:
    st.write("**Current tasks:**")
    df_tasks = st.session_state.tasks
    st.table(df_tasks)
    
    if st.button("🗑️ Clear all tasks"):
        st.session_state.tasks = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

# Load and use a simple local knowledge base for RAG-style guidance
kb_entries = load_knowledge_base()

st.divider()

st.subheader("💡 Ask PawPal+ for pet-care guidance")
st.caption("Use a small local knowledge base to get helpful pet-care advice based on your chosen species and tasks.")
rag_query = st.text_input("What would you like to know?", value="How should I care for this pet today?")
if st.button("🧠 Get guidance"):
    if not rag_query.strip():
        st.warning("Please enter a question.")
    else:
        pet_context = f"Species: {species}; pet name: {pet_name}"
        if st.session_state.tasks:
            task_names = ", ".join(task["name"] for task in st.session_state.tasks)
            full_query = f"{rag_query} Context: {pet_context}; current tasks: {task_names}"
        else:
            full_query = f"{rag_query} Context: {pet_context}"
        answer = build_rag_answer(full_query, kb_entries)
        st.write(answer)

st.divider()

st.subheader("🎯 Generate Your Daily Schedule")

if st.button("📅 Generate schedule", type="primary"):
    if not owner_name or not pet_name:
        st.error("Please enter owner and pet names.")
    elif not st.session_state.tasks:
        st.error("Please add at least one task.")
    else:
        try:
            # Create Owner instance
            owner = Owner(
                name=owner_name,
                available_start=time(7, 0),
                available_end=time(23, 0)
            )
            
            # Create Pet instance
            pet = Pet(
                name=pet_name,
                species=species,
                age=pet_age
            )
            
            # Convert priority strings to Priority enum
            priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
            
            # Create Task objects from form inputs
            tasks = []
            for task_data in st.session_state.tasks:
                task = Task(
                    name=task_data["name"],
                    type=task_data["type"],
                    priority=priority_map[task_data["priority"]],
                    duration_minutes=task_data["duration_minutes"],
                    frequency="daily"
                )
                tasks.append(task)
            
            # Add tasks to pet
            pet.tasks = tasks
            owner.add_pet(pet)
            
            # Generate schedule using Scheduler
            scheduler = Scheduler(owner, pet)
            schedule = scheduler.generate_daily_schedule(tasks)
            
            # Display schedule
            st.success("✅ Schedule generated!")
            st.markdown("### 📋 Your Daily Plan")
            st.info(schedule.get_schedule_summary())
            
            # Validation
            validation = scheduler.validate_schedule(schedule)
            if validation["is_valid"]:
                st.success("✓ Schedule is valid and feasible!")
            else:
                st.warning("⚠️ Schedule has some issues:")
                for issue in validation["issues"]:
                    st.write(f"- {issue}")
        
        except Exception as e:
            st.error(f"Error generating schedule: {e}")
