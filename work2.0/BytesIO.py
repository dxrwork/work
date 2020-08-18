>>>> from io import BytesIO
>>>> f = BytesIO()
>>>> f.write('жпнд'.encode('utf-8'))
>6
>>>> print(f.getvalue())
>b'\xe4\xb8\xad\xe6\x96\x87'
>