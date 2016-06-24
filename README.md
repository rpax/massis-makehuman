# About

## What is this
_massis-makehuman_ is a tool for adding animations to 3D models created with [makehuman][2]. Works seamessly with [mixamo][1] but might work with other animations.

## Why has been developed

## Usage

### Dependencies

- Required:
 - [Docker][docker_url]. The installation instructions are here: https://www.docker.com/products/overview
 - python (2.7.11+)
 - _sidomo_ library for python
	Can be installed via pip

		sudo -H pip install 'git+https://github.com/deepgram/sidomo.git#egg=sidomo'
		
 - MakeHuman v1.1.0
    - [Makehuman tool][2]
    - Makehuman mhx2 plugin: The preferred format for exporting makehuman models is `mhx2`.
    	The plugin is available via [bitbucket][bb_rpax].
        Instructions:
        Download the [compressed file from bitbucket][bb_rpax].
        Extract the contents of the folder named `9_export_mhx2` into the makehuman plugin folder. (usually, _/usr/share/makehuman/plugins_). Normally, this requires root permissions for copying. After copying it, the correct permissions can be restored like this:

			sudo chmod -R ugo+r 9_export_mhx2
			

- Not required:
	- Blender. Although it is not _really necessary_ for generating the animated models, it is needed for opening them.
	
			sudo apt-get install blender
			


## Running

The tool is provided as a docker image. Although it can be run directly by calling `docker run...`, a helper script (`generate.py`) is provided.
Parameters:


| Name   | Description | Additional notes|
|--------|-------------|-------------|
| mhx2 | path to the mhx2 file| - |
| textures| path to the textures dir| Optional, if not provided, the folder named 'textures' present in the same folder of the mhx2 file will be used instead|
| animations| path to the animations zip file| - |
| outputfile| path to the blender output file| - |
| unpack    | if the included files should be unpacked (recommended)| Not implemented yet. By default is true|


## Example:

### Step 1: Designing the human model with makehuman

Open the makehuman app:

![makehuman welcome screen](http://i.imgur.com/fuXuBoj.png)

As can be seen, the tool allows modifying multiple properties of the model. Here we are going to do minimal modifications, just for illustrating purposes.

#### Adding clothes
Clicking in the _Materials_ tab, we can add different kinds of clothes. We are going to select _Male Casual suit_.
![](http://i.imgur.com/PnpmUtL.png)

#### Configuring the skeleton: CMU-MB

In order to work with the mixamo animations, the selected skeleton **must be** of type the _cmu-mb_.
The skeleton selection can be done in the _Pose/Animate_ tab.

![](http://i.imgur.com/JkTvQDk.png)

### Step 2: Export the model to mhx2.

The model can be exported clicking in the _File_ tab, selecting _Export_ and _Make Human Exchange (mhx2)_.
![](http://i.imgur.com/65gVcLF.png). Just select the folder where you want to export it.
> tip: Better if it is empty

### Step 2: Creating animations in Mixamo

- You should have an account created at [https://www.mixamo.com][1]. If not, create one.
- Clicking on the _upload_ button, upload the massis' compatible bvh skeleton. (`massis_base.bvh`)
	![](http://i.imgur.com/uCWY5na.png)
- Mixamo will do the mapping automagically, and we can start adding animations. Don't worry if the model is lying on the ground, that's ok.
	![](http://i.imgur.com/NgZGRB5.png)

- A good way for downloading animations is creating an _animation pack_. This can be easily done by clicking on the desired animation and later on the _Add to pack_ button.

![](http://i.imgur.com/Azpx70E.png).

- After adding several animations (In the example, Guitar Playing, Jogging and running, all of them with the option _in Place_ checked), we can proceed to downloading the our pack.

- The download options should be as follows:
 - Format: Biovision (.bvh)
 - Frames per second : does not matter. 30 fps is ok.
 - Pose: No Character
 - KeyFrame Reduction: none
 ![](http://i.imgur.com/ctjpzeU.png)

After clicking _Queue Download_, the zip file will be ready for download.

### Step 3: Merging the animations

1. Ensure you have the latest docker image:
		docker pull rpax/massis-makehuman

2. Run the script
        $ generate.py --mhx2 <path-to-the-exported-mhx2> \
        --animations <path-to-mixamo-animations-zip> \
        --output <path-to-output-blend-file>

3. (Optional) open blender and check if the animations are ok.

![](http://i.imgur.com/or6jdzY.png)


### Extra: Importing to JME3.

Lo importas, boton derecho sobre el modelo, generate tangents, en las geometrias transparentes le das a create j3m file, y editas el j3m. Quitas las texturas alpha.




[1]: https://www.mixamo.com
[2]: http://www.makehuman.org/
[bb_rpax]: https://bitbucket.org/rpax/mhx2-makehuman-exchange/downloads
[docker_url]: https://www.docker.com/












