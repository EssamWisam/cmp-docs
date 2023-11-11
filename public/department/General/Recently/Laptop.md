# 💻 Choosing a Laptop

Generally, the minimum needed specs for a laptop are not that high. Let's begin by quickly going over the main parts of the laptop. Each part will get its own brief section. It's advised that you at least skim through this whole document once.

Note that unlike desktop PCs where you can mostly mix and match parts, laptops come mostly as a whole package. You're usually able to upgrade the storage/RAM, but that's it. So you're stuck with whatever choose until you upgrade to a new laptop. Make sure to plan a little ahead and be prepared to strech your budget if you plan on keeping your laptop for long (5+ years).

## Picking a laptop in a nutshell
Set a budget range, filter out all laptops that don't fit your range or aren't in stock, filter out laptops that dont fit your usage, the watch as many reviews as you can for each laptop so you get to know the pros and cons for each. You can then settle on one and buy it. Keep in mind that you can buy from Egypt for local warranty (for what it's worth), or from outside if you want to save money.

## Laptop types
Laptops generally fall under three broad types: thin and light, gaming, and workstation laptops.

### Thin and Lights
This type of laptop sacrifices performance and sometimes upgradability for the sake of being the most portable with the smallest chargers and longest battery life. You usually will have to pay more for similar specs to other types while receiving lower performance due to inferior cooling or power budget.

### Gaming 
Performance at the cost of everything else. These are heavy and hot, but they sure (usually) run fast. They also don't last long, be prepared to carry around a heavy power brick if you intend on doing more than one hour of work unplugged. You also pay a price premium for the GPU. So make sure you're going to use it before settling on one.

### Workstations
Sometimes even bulkier than gaming laptops, these laptops are usually bought used as they provide good-ish performance for cheap. They usually have higher end but older parts. Since they are usually bought used, they can hide nasty surprises. Make sure to test them well before buying.

## Laptop parts
This section dissuses the main parts that you should compare laptops over.

### CPU
The brains of the laptop. This will contribute greatly to how smooth and responsive your experience is with the laptop. These are usually called "Intel Core i7 9750H",  "AMD Ryzen 5 5500U", etc.. Let's begin by breaking down the naming convention.

#### Naming Convention
##### Manufacturer
(Intel/AMD): These are the biggest two names in laptop processors at the time of writing (if we ignore apple for a minute), they're usually about equal, we'll discuss them a bit later on. 

##### Family
(Core iX, Ryzen X): This is a way for each manufacturer to separate their processors into larger groups where each is aimed at a specific purpose. As a general rule, you have the server, enthusiast, mainstream, and budget groups. These correspond to Xeon, i9, i7/i5/i3, and celeron/pentium CPUs for Intel, and EPYC, ThreadRipper/Ryzen 9, Ryzen 7/5/3, and Athlon CPUs for AMD. We'll focus on mainstream families in this document as they're about good enough for CMP work, but not too expensive/high end for most people. 

##### Model/Number
For example "9750", "12600" for intel, and "5500", "7840". This usually indicates some performance ordering ***in the same generation and series***. So a Ryzen 7 7840U is likely more performant that a Ryzen 7 7730U. Tldr; bigger is better, with some caveats. 

##### Series
This is the "H" or "U" in intel processors, or "HX"/"HS" or "U" in AMD processors. In short, "H"/"HX"/"HS" processors perform better, but have worse battery life, consume more power, and require more cooling than their "U" counterparts.

#### Comparisons
One must note that one processor can perform very differently with different power consumption limits and different cooling systems, this must be taken in mind when comparing two laptops with the same processor but vastly different cooling systems or power limits.

Another thing that must be taken in mind is that inter-series comparisons must be understood correctly. You cannot compare an F1 car to a gas efficient consumer car. Each is designed for a specific purpose and this must be kept in mind. You use one when you want to go _FAST_, and the other if you like your rides to be comfortable and cheap. This also applies to inter-generational comparisons, it's expected that the more recent version of a CPU _should_ be better. 

Some other metrics that you can compare based on are: frequency and number of cores. The frequency usually affects the speed of a single core, while the number of cores usually affects how many tasks you can do in parallel. For both, the higher, the better. But as always things are much more nuanced that can be explained in this humble document. Your best bet is to read/watch a lot of reviews so you can get a general idea about the relative ordering between the different CPUs.

In a nutshell: CPUs have multiple dimensions to compare based upon: cooling, power consumption, frequency, number of cores, and much more. Determining your usecase and using information from reviews will generally guide you in the right direction.

### RAM
Mainly contributes to how many applications you can run in parallel. Generally, the higher the ram capacity and frequency are, the better it is. So for example, an 8GB stick of ram is usually better than a 4GB stick of ram. And similarly, a "3200MHz" stick of ram is also better than a "2666MHz" stick of ram. Another dimension to consider is the number of sticks coming with the laptop. Usually, having two sticks installed is better than one for performance, even if the total capacity is the same. So 2x8GB is usually better than 1x16GB. Capacity is more important than frequency here.

If your budget is tight and the laptop comes with only one stick, you can later add another stick (check the laptop spec sheet or a teardown for this, keep in mind the model) if needed. If your laptop comes with one slot or two filled slots, you can always sell a stick or two off and buy a better one.

Note that some laptops (mostly thin and light ones or budget ones) come with soldered ram, *YOU WILL NOT BE ABLE TO UPGRADE*, so make sure to overprovision.

You'll be running a lot of things that are ram hungry for projects and labs, so the bare minimum you should aim for is 8GB (terrible idea by the way), 16GB+ is strongly preferred if possible. 

### Screen
#### Resolution
Displays contents from the laptop. You'll be staring at this for hours every day. It's advised to at least aim for 1920x1080 for the resolution. You can live with lower resolutions, but they won't be super pleasant.

#### Color
If you intend to do color related work (graphic design, video editing, etc..), or want to have good and saturated/accurate colors, make sure to check the laptop color coverage, it's usually stated as "72% sRGB" or "45% NTSC" in the spec sheet. The higher, the better (and more expensive). The author prefers 72%+ NTSC.

#### Brightness
Screen brightness is another important point, it's usually measured in "nits". For example, a good screen will have 300+ nits. Any less and it might be too dim for use here you have strong lighting.

#### Panel Type
You'll probably meet IPS/TN screens in different laptops, here's the difference in a nutshell: TN is cheaper but has worse colors, while IPS is the opposite.

#### Finish
Another thing that you might encounter is the screen finish: matt screens have slightly less saturated colors but can be used outside or in bright light, while glossy screens are the opposite.

### Cooling
Allows your laptop to perform well for longer periods of time. The better the cooling is, the harder and longer your laptop will be able to perform. Some notable parts include vents (one at minimum), number of fans (also one at minimum). Some laptops might have more than one vent for each fan (one to the side and another for the back for each fan, for example), other laptops have multiple fans using a wider vent. Generally, the more surface area you have, the better. Surface area here is affected by both the width/number of vents, and the height/thickness. The more cooling you have, the heavier the laptop will be.

You usually cannot compare laptops by these specs alone, it's advised you pick two different laptop chassis with similar specs and watch/read reviews and compare thermals (averge, max temperature as well as CPU/GPU power).

### Battery
Controls how long/hard you can run your laptop without the charger. Larger capacity (Watt-hours or "wh") is generally better, but might lead to a heavier weighing laptop.

### Chasis
The skeleton of your laptop. Mainly determines how rugged/premium your laptop feels. The more money you spend, the more rigid the chassis will be, with more premium materials (aluminum vs plastic). Screen hinges are also a notable part. Some laptops are known to have widespread hinge failures, so make sure to look those up.

### Inputs
Mainly the keyboard and mouse. You can't really eye this, so you either have to go and test a real-life laptop in some store, or watch reviews. You can always use an external mouse/keyboard, but keep in mind that you'll have to carry it with you, and it will take up USB ports.

### Storage Drives
Controls how much stuff you can download (pirate) from the internet. Storage drives have two types: NVMe SSDs and SATA HDDs (ignoring SATA SSDs since they aren't super popular for laptops.). The former is the faster, lighter, and (of course) more expensive option, while the latter allows you to get more storage capacity for cheaper. Some laptops come with only the former, some come only with the latter (cheaper ones), and some come with both. The author highly recommends at least an NVMe SSD for the OS (Windows or Linux). You can still live with a SATA HDD, but it will be SLOW (as in five minutes to boot slow vs 30 or less on an NVMe SSD).

You can always expand your storage (check the spec sheet for available ports), or use an external drive.

### Ports
Allows you to connect mice, keyboards, USBs, external harddrives, screens, etc.. to your laptop. Usually the more, the merrier. Mostly controlled by the laptop chassis. The author recommends at least 2 USB-A ports (the big rectangular ones), a USB-C port (the small, round ones), and an HDMI port as a minimum. Other nice to have ports include: a headphone port, an ethernet port, more USB/USB-C ports.

### (Optional) GPU
Mostly matters for gamers. For machine/deep learning aficionados, you'll probably use some cloud platform to train your models. 

You want to aim for an nvidia RTX xx60 or higher, but an nvidia RTX xx50 can also do the job if you're willing to lower the settings. The corresponding GPUs on AMDs side are the RX x600/700 and x500 respectively. The author (begrudgingly) recommends nvidia GPUs over AMD GPUs (at the time of writing at least)

GPU comparisons are similar to CPU comparisons: make sure to keep in mind the power limit. The exact same GPU running at 130 watts obviously performs better than at 90 watts for performance, but outputs more heat thus requiring more cooling and a beefier power brick.
