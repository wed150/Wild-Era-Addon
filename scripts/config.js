//配置文件
export let Config = {
    immune:{
        attack:{
            [EntityDamageCause.entityAttack]:[
                "minecraft:diamond_helmet"//可以免疫生物攻击(小于生命)的头盔
            ],
            [EntityDamageCause.projectile]:[
                "minecraft:diamond_helmet"//可以免疫弹射物攻击(小于生命)的头盔
            ]
        },
        effect:[
            "minecraft:diamond_helmet"//可以免疫药水效果的头盔
        ]
    },
    canRot:{
        "minecraft:diamond_helmet":"minecraft:rotten_flesh",
        "minecraft:mushroom_stew":"minecraft:rotten_flesh",
        /*"原物品id":"腐烂后物品id",*/
    },
    rotTime:240/*00*/,
    attackEvent:{
        addEffect:{
            "minecraft:diamond_helmet":{
                effect: [
                    {
                        "effectId":"minecraft:slowness",
                        "duration":80,
                        "amplifier":1
                    }
                ]
            },
            "minecraft:golden_helmet":{
                effect: [
                    {
                        "effectId":"minecraft:poison",
                        "duration":120,
                        "amplifier":1
                    }
                ]
            },
            "minecraft:iron_helmet":{
                effect: [
                    {
                        "effectId":"minecraft:weakness",
                        "duration":160,
                        "amplifier":1
                    }
                ]
            },
            "minecraft:chainmail_helmet":{
                effect: [
                    {
                        "effectId":"minecraft:levitation",
                        "duration":200,
                        "amplifier":1
                    }
                ]
            },
            "minecraft:netherite_helmet":{
                effect: [
                    {
                        "effectId":"minecraft:wither",
                        "duration":240,
                        "amplifier":1
                    }
                ]
            },
            "minecraft:leather_helmet":{
                effect: [
                    {
                        "effectId":"minecraft:wither",
                        "duration":240,
                        "amplifier":1
                    },
                    {
                        "effectId":"minecraft:weakness",
                        "duration":240,
                        "amplifier":1
                    }
                ]
            }
            /*
            "物品id":{
                effect: [
                    {
                        "effectId":"效果id",
                        "duration":时间(tick),
                        "amplifier":效果等级
                    },
                    {…………}
                ]
            }
            */
        },
        spwamEntity:{
            "minecraft:diamond_sword":"minecraft:lightning_bolt"
            /*"攻击物品id":"生成的生物"*/

        }
    },
    bark:"minecraft:rotten_flesh",//树皮id
    durability:[
        "minecraft:diamond_pickaxe",
    ]
};














//Debug配置
import {CommandPermissionLevel, EntityDamageCause, system, world} from "@minecraft/server";

export let debug = false;
system.beforeEvents.startup.subscribe(event=>{
    event.customCommandRegistry.registerCommand( {
        name: "mode:debug",
        description: "切换 Debug Mode",
        permissionLevel: CommandPermissionLevel.GameDirectors,
    },() => {
        debug = !debug;
        world.sendMessage(`Debug mode ${debug ? "enabled" : "disabled"}`);
    })
})