resource "libvirt_domain" "ipa-server" {
  name   = "tang"
  memory = "2048"
  vcpu   = 2
  autostart = true
  qemu_agent = true
  xml {
    xslt = <<-EOT
      <?xml version="1.0" ?>
      <xsl:stylesheet version="1.0"
                      xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:output omit-xml-declaration="yes" indent="yes"/>

        <!-- Copy everything from the generated XML -->
        <xsl:template match="node()|@*">
          <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
          </xsl:copy>
        </xsl:template>

        <!-- Set domain#type to 'qemu' for nested virtualization -->
        <xsl:template match="/domain/@type">
          <xsl:attribute name="type">
              <xsl:value-of select="'qemu'"/>
          </xsl:attribute>
        </xsl:template>

      </xsl:stylesheet>
    EOT
  }

  network_interface {
    network_name = "virtnet"
    addresses = ["172.16.2.2"]
  }

  disk {
    volume_id = "${libvirt_volume.ipa-root.id}"
    scsi = true
  }

  cloudinit = "${libvirt_cloudinit_disk.ipa-cloud-init.id}"

  console {
    type = "pty"
    target_type = "serial"
    target_port = "0"
  }

}
