Now you should be able to run the compile command successfully:
`python manage.py shell`
Then in the shell:

```py
from chatbot.compile_proto import compile_proto
compile_proto()
```

This will compile your proto files into Python modules that you can import and use in your application.
