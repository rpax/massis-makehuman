package com.massisframework.makehuman;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

import org.apache.commons.io.FilenameUtils;

import com.jme3.animation.SkeletonControl;
import com.jme3.app.SimpleApplication;
import com.jme3.asset.plugins.FileLocator;
import com.jme3.export.binary.BinaryExporter;
import com.jme3.scene.Geometry;
import com.jme3.scene.Node;
import com.jme3.system.JmeContext.Type;
import com.jme3.util.TangentBinormalGenerator;


public class BlenderConverter extends SimpleApplication {

	public static void main(String[] args)
	{
		BlenderConverter app = new BlenderConverter();
		app.start(Type.Headless);
	}

	@Override
	public void simpleInitApp()
	{
		String workingDir = System.getProperty("massis3.workingDir");
		workingDir = Paths.get(workingDir).toFile().getAbsolutePath();
		Path outputPath = Paths.get(workingDir);
		
		assetManager.registerLocator(outputPath.toFile().getAbsolutePath(),
				FileLocator.class);
		try
		{

			List<String> models = Files.walk(outputPath)
					.filter(path -> path.toString().endsWith(".blend"))
					.map(outputPath::relativize)
					.map(Path::toString)
					.collect(Collectors.toList());

			for (String modelP : models)
			{
				Node n = (Node) assetManager.loadModel(modelP);
				n = prepare(n);

				// Guardamos.
				String baseName = FilenameUtils.getBaseName(modelP);
				File realModelFile = outputPath
						.resolve(modelP)
						.getParent()
						.resolve(baseName + ".j3o")
						.toFile();

				BinaryExporter exporter = BinaryExporter.getInstance();
				exporter.save(n, realModelFile);
			}
			this.stop();

		} catch (Exception e)
		{
			e.printStackTrace();
		}

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
