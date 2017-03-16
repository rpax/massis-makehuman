package com.massisframework.makehuman;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.logging.ConsoleHandler;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.LogManager;
import java.util.logging.Logger;
import java.util.stream.Collectors;

import org.apache.commons.io.FilenameUtils;

import com.jme3.animation.SkeletonControl;
import com.jme3.app.SimpleApplication;
import com.jme3.asset.plugins.FileLocator;
import com.jme3.export.binary.BinaryExporter;
import com.jme3.scene.Geometry;
import com.jme3.scene.Node;
import com.jme3.scene.plugins.blender.meshes.Face;
import com.jme3.system.JmeContext.Type;
import com.jme3.util.TangentBinormalGenerator;
import com.massisframework.massis3.util.optimize.FastLodGenerator;

public class BlenderConverter extends SimpleApplication {

	private static String WORKING_DIR;

	public static void main(String[] args)
	{
		WORKING_DIR = System.getProperty("massis3.workingDir");
		if (WORKING_DIR == null || WORKING_DIR.isEmpty())
			return;
		
		BlenderConverter app = new BlenderConverter();
		app.start(Type.Headless);
	}

	@Override
	public void simpleInitApp()
	{
		LogManager.getLogManager().reset();
		Logger globalLogger = Logger.getLogger(java.util.logging.Logger.GLOBAL_LOGGER_NAME);
		globalLogger.setLevel(java.util.logging.Level.SEVERE);
		
		String workingDir = WORKING_DIR;
		workingDir = Paths.get(workingDir).toFile().getAbsolutePath();
		Path outputPath = Paths.get(workingDir);

		assetManager.registerLocator(outputPath.toFile().getAbsolutePath(),
				FileLocator.class);
		try
		{
			
			List<String> models = Files.walk(outputPath)
					.filter(path -> path.toString().endsWith(".blend"))
					.map(outputPath::relativize).map(Path::toString)
					.collect(Collectors.toList());

			setClassLoggingLevel(Face.class,Level.SEVERE);
			setClassLoggingLevel(TangentBinormalGenerator.class,Level.SEVERE);
			
			for (String modelP : models)
			{
				
				Node n = (Node) assetManager.loadModel(modelP);
				n = prepare(n);

			
				String baseName = FilenameUtils.getBaseName(modelP);
				File realModelFile = outputPath.resolve(modelP).getParent()
						.resolve(baseName + ".j3o").toFile();

				//Generate LODS -> disable
				FastLodGenerator.bakeAllLods(n, 1, 0.7f,0.8f,0.9f);
				BinaryExporter exporter = BinaryExporter.getInstance();
				exporter.save(n, realModelFile);
			}
			this.stop();

		} catch (Exception e)
		{
			e.printStackTrace();
		}

	}

	private static void setClassLoggingLevel(Class<?> class1, Level lvl)
	{
		Logger faceLogger = Logger.getLogger(class1.getName());
		Handler consoleHandler = new ConsoleHandler();
		consoleHandler.setLevel(lvl);
		faceLogger.setUseParentHandlers(false);
		Handler[] handlers = faceLogger.getHandlers();
		for (int i = 0; i < handlers.length; i++)
		{
			faceLogger.removeHandler(handlers[i]);
		}
		faceLogger.setLevel(lvl);
		faceLogger.addHandler(consoleHandler);
		
	}

	private static Node prepare(Node n)
	{
		Node[] wrapper = new Node[1];

		n.depthFirstTraversal(s -> {
			if (s instanceof Geometry)
			{
				((Geometry) s).getMaterial().clearParam("AlphaMap");
				((Geometry) s).getMaterial().clearParam("Shininess");
			}
			if (s.getControl(SkeletonControl.class) != null)
			{
				wrapper[0] = (Node) s;
			}
		});
		TangentBinormalGenerator.generate(wrapper[0]);
		return wrapper[0];
	}

}
