# How to template with Jinja2 (.j2 file extentions)

On the Flutter front end, what actually happens when we start the unit test?

![Alt text](image-2.png)

When we click the `Run single test` button

![Alt text](image-1.png)

In this example for the `ThreeSum` unit test.

![Alt text](image.png)

Inside the terminal we can see the blue text start to populate.

This is a direct result from:
```freshGPT\autogpts\testgpt\forge\prompts\gpt-3.5-turbo\system-format.j2```

![Alt text](image-3.png)

Here is where the `what` key value pair is displayed from the addition diff on line 6:

![Alt text](image-4.png)

This is directly correlated to line 113-114 of
```autogpts\testgpt\forge\agent.py```:

```
        # Load the system and task prompts
        system_prompt = prompt_engine.load_prompt("system-format")
```

![Alt text](image-5.png)

Another important thing to note is the architecture formed with the sub folders.

Note inside the forge folder. We are able to access the `PromptEngine` with the string "gpt-3.5-turbo" on line 111 of `autogpts\testgpt\forge\agent.py`

Then we are able to directly access `autogpts\testgpt\forge\prompts\gpt-3.5-turbo\system-format.j2` on line 114 with the `load_prompt` method.

![Alt text](image-6.png)

Building off of the `tutorials\003_crafting_agent_logic.md`

    # Load the task prompt with the defined task parameters
    task_prompt = prompt_engine.load_prompt("task-step", **task_kwargs)

    # Append the task prompt to the messages list
    messages.append({"role": "user", "content": task_prompt})

![Alt text](image-7.png)

We can append additional templating for our prompt engineering.

TODO: Document additional details on Jinja specifics.