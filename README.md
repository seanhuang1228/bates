# Bates

A easy bates number generator, which will add Bates number at the bottom-left corner.

## Usage

```
python bates.py [option] filename
```

The `filename` is the base pdf file you want to add bates number on.

## Options

### Start Number

You can setting the number where the bates number starts with option `-s`, for example:

```
python bates.py -s 2000 example.pdf
```

And the bates number will start from 2000.

Default value is 1000.

### Copies Count

You can set the number of file you want to generate with option `-n`, for example:

```
python bates.py -n 100 example.pdf
```

This will generate 100 copies of example.pdf, and they will be assigned bates number from 1000 to 1099.

Default value is 1

### Prefix String

You can set the prefix string you want to append before the Bates number with option `-p`, for example:

```
python bates.py -p PRE- example.pdf
```

The gerneated pdf will be with the `PRE-1000` on the bottom-left corner.

Default value is an empty string.
